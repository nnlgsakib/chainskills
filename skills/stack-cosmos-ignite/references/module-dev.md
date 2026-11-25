# Writing module code (Cosmos SDK v0.53+ style, as scaffolded by Ignite v29)

Checked 2026-11-25 against Ignite v29.10.1 templates (`ignite/templates/module/create`, `typed/list`): keeper fields (`corestore.KVStoreService`, `codec.Codec`, `address.Codec`, `authority []byte`, collections `Schema`/`Params`, `<Type>Seq` + `<Type>`), errors registered from code 1100, `query.CollectionPaginate`, and address validation in msg servers.

**SDK v0.55 chains (Ignite v30):** imports change. `cosmossdk.io/log` becomes `cosmossdk.io/log/v2`. `cosmossdk.io/store/types` becomes `github.com/cosmos/cosmos-sdk/store/v2/types`. `cosmossdk.io/x/{evidence,feegrant,upgrade}` become `github.com/cosmos/cosmos-sdk/x/...`. `x/params` is gone, and module constructors drop the subspace argument. The patterns below stay the same.

Match the scaffolded project. If the keeper uses `collections`, keep using it; if the project is on an older SDK with raw `prefix.Store`, follow that instead.

## Contents
- Layout
- Keeper with collections
- Msg server pattern
- Authority-gated messages
- Queries and pagination
- Errors
- Events
- Genesis
- AutoCLI
- Tests

## Layout

```
proto/<chain>/<module>/v1/{tx,query,genesis,params,<types>}.proto
x/<module>/keeper/     keeper.go, msg_server_*.go, query_*.go, *_test.go
x/<module>/types/      codec.go, errors.go, keys.go, genesis.go, expected_keepers.go, *.pb.go
x/<module>/module/     module.go, depinject.go, autocli.go, genesis.go, simulation.go
app/app.go, app/app_config.go   (depinject wiring)
```

## Keeper with collections

```go
type Keeper struct {
	cdc          codec.Codec
	addressCodec address.Codec
	storeService corestore.KVStoreService
	authority    []byte // gov module account by default

	bankKeeper types.BankKeeper

	Schema  collections.Schema
	Params  collections.Item[types.Params]
	PostSeq collections.Sequence
	Post    collections.Map[uint64, types.Post]
	// Secondary index example: posts by author
	PostsByAuthor collections.KeySet[collections.Pair[sdk.AccAddress, uint64]]
}
```

- Prefixes (`collections.NewPrefix(n)`) are part of consensus state. Never change or reuse one after launch.
- Need lookups by another field? Add an index (`KeySet` of pairs, or `indexes.Multi` with `IndexedMap`) instead of iterating everything.

## Msg server pattern

```go
func (k msgServer) TipPost(ctx context.Context, msg *types.MsgTipPost) (*types.MsgTipPostResponse, error) {
	sender, err := k.addressCodec.StringToBytes(msg.Creator)
	if err != nil {
		return nil, errorsmod.Wrap(sdkerrors.ErrInvalidAddress, err.Error())
	}
	if !msg.Amount.IsValid() || !msg.Amount.IsPositive() {
		return nil, errorsmod.Wrap(sdkerrors.ErrInvalidCoins, msg.Amount.String())
	}

	post, err := k.Post.Get(ctx, msg.Id)
	if errors.Is(err, collections.ErrNotFound) {
		return nil, errorsmod.Wrapf(types.ErrPostNotFound, "id %d", msg.Id)
	} else if err != nil {
		return nil, err
	}

	author, err := k.addressCodec.StringToBytes(post.Creator)
	if err != nil {
		return nil, err
	}
	if err := k.bankKeeper.SendCoins(ctx, sender, author, sdk.NewCoins(msg.Amount)); err != nil {
		return nil, err
	}

	post.TotalTips = post.TotalTips.Add(msg.Amount.Amount) // math.Int, never float
	if err := k.Post.Set(ctx, msg.Id, post); err != nil {
		return nil, err
	}

	if err := sdk.UnwrapSDKContext(ctx).EventManager().EmitTypedEvent(&types.EventPostTipped{
		Id: msg.Id, Sender: msg.Creator, Amount: msg.Amount,
	}); err != nil {
		return nil, err
	}
	return &types.MsgTipPostResponse{Tipped: true}, nil
}
```

Validation rules:
- Every address string → `addressCodec.StringToBytes`.
- Every string → max length (constants in `types/`), prevents state bloat.
- Every amount → valid, positive, correct denom if restricted.
- Every slice → max length.
- Check existence/ownership before writing.
- Do the checks before any state write: a failed tx reverts state, but early rejection costs less gas and keeps logic readable.

Use `sdkCtx.HeaderInfo().Time` (or `BlockTime()`) for time, `HeaderInfo().Height` for height.

## Authority-gated messages

Param updates and admin actions must only be executable by governance:

```go
func (k msgServer) UpdateParams(ctx context.Context, req *types.MsgUpdateParams) (*types.MsgUpdateParamsResponse, error) {
	authority, err := k.addressCodec.StringToBytes(req.Authority)
	if err != nil {
		return nil, errorsmod.Wrap(err, "invalid authority address")
	}
	if !bytes.Equal(k.GetAuthority(), authority) {
		return nil, errorsmod.Wrapf(types.ErrInvalidSigner, "expected %s got %s", k.addressCodec.BytesToString(k.GetAuthority()), req.Authority)
	}
	if err := req.Params.Validate(); err != nil {
		return nil, err
	}
	return &types.MsgUpdateParamsResponse{}, k.Params.Set(ctx, req.Params)
}
```

Implement `Params.Validate()` with real bounds — gov proposals can set anything otherwise.

## Queries and pagination

```go
func (q queryServer) ListPost(ctx context.Context, req *types.QueryAllPostRequest) (*types.QueryAllPostResponse, error) {
	if req == nil {
		return nil, status.Error(codes.InvalidArgument, "invalid request")
	}
	posts, pageRes, err := query.CollectionPaginate(ctx, q.k.Post, req.Pagination,
		func(_ uint64, v types.Post) (types.Post, error) { return v, nil })
	if err != nil {
		return nil, status.Error(codes.Internal, err.Error())
	}
	return &types.QueryAllPostResponse{Post: posts, Pagination: pageRes}, nil
}
```

Never return unbounded lists from queries.

## Errors

```go
// types/errors.go — codes start at 2 (1 is reserved), never renumber after release
var (
	ErrInvalidSigner = errorsmod.Register(ModuleName, 1100, "expected gov account as only signer for proposal message")
	ErrPostNotFound  = errorsmod.Register(ModuleName, 1101, "post not found")
)
```

## Events

Define events in proto (`message EventPostTipped {...}`) and emit with `EmitTypedEvent`. Indexers and frontends depend on them — treat event schema like API.

## Genesis

- `GenesisState.Validate()` checks duplicates, ID < next sequence, addresses valid, params valid.
- `InitGenesis` restores sequences (`PostSeq.Set(ctx, gs.PostCount)`), `ExportGenesis` writes them back.
- Round-trip test: init → export → compare.

## AutoCLI

`x/<module>/module/autocli.go` maps RPCs to CLI commands. When adding a msg/query by hand (not via scaffold), add its entry there with `PositionalArgs`. Set `Skip: true` for gov-only msgs like `UpdateParams`.

## Tests

```go
func TestTipPost_Rejects(t *testing.T) {
	f := initFixture(t) // scaffolded test fixture in keeper/ (name may differ)
	ms := keeper.NewMsgServerImpl(f.keeper)
	cases := []struct{ name string; msg *types.MsgTipPost; err error }{
		{"bad address", &types.MsgTipPost{Creator: "nope"}, sdkerrors.ErrInvalidAddress},
		{"zero amount", &types.MsgTipPost{Creator: f.addrs[0], Amount: sdk.NewInt64Coin("umychain", 0)}, sdkerrors.ErrInvalidCoins},
		{"missing post", &types.MsgTipPost{Creator: f.addrs[0], Id: 99, Amount: sdk.NewInt64Coin("umychain", 1)}, types.ErrPostNotFound},
	}
	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			_, err := ms.TipPost(f.ctx, tc.msg)
			require.ErrorIs(t, err, tc.err)
		})
	}
}
```

Use mocks (gomock / scaffolded `testutil`) for `expected_keepers.go` interfaces in unit tests; use the full app in integration tests.
