# Writing an Ignite App

Ignite Apps are standalone Go binaries that Ignite runs as gRPC plugins (hashicorp/go-plugin). The examples target `github.com/ignite/cli/v29`. For Ignite v30 (release candidate, 2026-11-25), replace every `cli/v29` import and the go.mod require with `cli/v30`, then rebuild the plugin (docs.ignite.com/migration/v30.0.0). Use one when you want a repeatable `ignite <something>` command or a hook around `ignite chain build/serve` for your team or the community.

## Scaffold and install

```bash
ignite app scaffold my-app              # creates ./my-app (Go module)
cd my-app && go build ./...
ignite app install -g $(pwd)            # absolute path, global
ignite my-app --help
```

Each run of an `ignite my-app` command rebuilds the plugin from source if it changed, so the dev loop is: edit → rerun the command.

## Layout (as in github.com/ignite/apps)

```
my-app/
├── cmd/            command definitions + handlers
├── integration/    app_test.go (integration tests against real ignite)
├── main.go         Manifest + Execute + hooks + plugin.Serve
├── go.mod          requires github.com/ignite/cli/v29
├── CHANGELOG.md
└── README.md
```

## main.go

```go
package main

import (
	"context"
	"errors"
	"fmt"
	"strings"

	hplugin "github.com/hashicorp/go-plugin"
	"github.com/ignite/cli/v29/ignite/services/plugin"

	"github.com/org/my-app/cmd"
)

type app struct{}

func (app) Manifest(context.Context) (*plugin.Manifest, error) {
	return &plugin.Manifest{
		Name:     "my-app",
		Commands: cmd.GetCommands(),
		Hooks: []*plugin.Hook{
			{Name: "after-build", PlaceHookOn: "ignite chain build"},
		},
	}, nil
}

func (app) Execute(ctx context.Context, c *plugin.ExecutedCommand, api plugin.ClientAPI) error {
	// Pattern used by official apps: dispatch on the raw args.
	// c.OsArgs = ["ignite", "my-app", "hello", ...]
	args := c.OsArgs[2:]
	if len(args) == 0 {
		return errors.New("missing subcommand")
	}
	switch args[0] {
	case "hello":
		return cmd.HelloHandler(ctx, c, api)
	default:
		return fmt.Errorf("unknown command: %s", strings.Join(c.OsArgs, " "))
	}
}

func (app) ExecuteHookPre(ctx context.Context, h *plugin.ExecutedHook, api plugin.ClientAPI) error {
	info, err := api.GetChainInfo(ctx) // chain-id, rpc address, app path, home...
	if err != nil {
		return err
	}
	_ = info
	return nil
}
func (app) ExecuteHookPost(context.Context, *plugin.ExecutedHook, plugin.ClientAPI) error    { return nil }
func (app) ExecuteHookCleanUp(context.Context, *plugin.ExecutedHook, plugin.ClientAPI) error { return nil }

func main() {
	hplugin.Serve(&hplugin.ServeConfig{
		HandshakeConfig: plugin.HandshakeConfig(),
		Plugins:         map[string]hplugin.Plugin{"my-app": plugin.NewGRPC(&app{})},
		GRPCServer:      hplugin.DefaultGRPCServer,
	})
}
```

## Commands with flags

```go
func GetCommands() []*plugin.Command {
	return []*plugin.Command{{
		Use:     "my-app [command]",
		Aliases: []string{"ma"},
		Short:   "My team's chain tooling",
		Commands: []*plugin.Command{{
			Use:   "hello [name]",
			Short: "Say hello",
			Flags: []*plugin.Flag{{
				Name: "path", Shorthand: "p", Usage: "path of the chain",
				Type: plugin.FlagTypeString, DefaultValue: ".",
			}},
		}},
	}}
}

func HelloHandler(ctx context.Context, c *plugin.ExecutedCommand, _ plugin.ClientAPI) error {
	flags := plugin.Flags(c.Flags)
	path, err := flags.GetString("path")
	if err != nil {
		return err
	}
	_ = path
	_ = c.Args
	return nil
}
```

Hooks: `PlaceHookOn` takes the full command (`"ignite chain build"`, `"ignite chain serve"`, `"ignite scaffold chain"`). Pre runs before, Post after success, CleanUp always.

To add flags to an existing Ignite command (like fee-abstraction adds `--fee-abstraction` to `ignite scaffold chain`), declare them on the hook — the flag values arrive in `hook.Flags` in the hook handlers:

```go
{
	Name:        "scaffold-chain",
	PlaceHookOn: "ignite scaffold chain",
	Flags: []*plugin.Flag{{
		Name: "my-feature", Usage: "include my feature",
		Type: plugin.FlagTypeBool, DefaultValue: "false",
	}},
}
```

## Modifying a user's chain code

Official apps (wasm, evm, evolve) use Ignite's own packages — reuse them instead of string-hacking:

- `github.com/ignite/cli/v29/ignite/services/chain` — `chain.New(path)` to load config, home, binary name, SDK version (`c.Version.LT(cosmosver.StargateFiftyVersion)` to gate).
- `github.com/ignite/cli/v29/ignite/pkg/xast` — AST edits: `AppendImports`, `ModifyFunction`, `ModifyStruct`, `InsertGlobal`, `AppendFunction`.
- `github.com/ignite/cli/v29/ignite/pkg/xgenny` + plush templates — generate files.
- `github.com/ignite/cli/v29/ignite/pkg/gocmd` — `ModTidy`, `Fmt`, `GoImports` after generation.
- `github.com/ignite/cli/v29/ignite/pkg/cliui` — spinners/status output.

Make edits idempotent (running `add` twice must not duplicate code) and fail with a clear message on unsupported Ignite/SDK versions.

## Testing

`integration/app_test.go` in official apps scaffolds a fresh chain with Ignite's `envtest`, installs the app from the local path, runs its commands and builds the chain. Copy that pattern; run with `go test ./integration/...` (slow — needs network and Go toolchain).

## Publishing

1. Own repo (or monorepo subfolder) with README, LICENSE, CHANGELOG, tags (`my-app/v0.1.0` for monorepo subfolders).
2. Users install with `ignite app install -g github.com/org/repo[/subdir][@tag]`.
3. List it in the Ignite app registry via PR so `ignite appregistry` finds it.
