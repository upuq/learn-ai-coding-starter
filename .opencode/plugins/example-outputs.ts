import { readdir } from "node:fs/promises"
import { join } from "node:path"
import { Plugin } from "@opencode/plugin"

const ENTRYPOINT = "sloperator.py"
// --no-active ignores an inherited VIRTUAL_ENV and uses the project's own .venv.
const UV_FLAGS = ["uv", "run", "--no-active"]

const EXAMPLES_DIRECTORY = "examples"

type ExampleResult = {
  name: string
  exitCode: number
  firstLine: string
}

export default Plugin.define({
  id: "example-outputs",
  async setup(ctx) {
    const root = ctx.location.directory

    await ctx.tool.transform((tools) => {
      tools.add({
        name: "example_outputs",
        description:
          "Run every examples/*.slop program and report each example's filename, exit code, " +
          "and first line of stdout.",
        input: {
          type: "object",
          properties: {},
          additionalProperties: false,
        },
        output: {
          type: "object",
          properties: {
            examples: {
              type: "array",
              items: {
                type: "object",
                properties: {
                  name: { type: "string" },
                  exitCode: { type: "integer" },
                  firstLine: { type: "string" },
                },
                required: ["name", "exitCode", "firstLine"],
                additionalProperties: false,
              },
            },
          },
          required: ["examples"],
          additionalProperties: false,
        },
        options: { codemode: false },
        async execute() {
          const examplesDirectory = join(root, EXAMPLES_DIRECTORY)
          const names = (await readdir(examplesDirectory))
            .filter((name) => name.endsWith(".slop"))
            .sort()

          const examples: ExampleResult[] = []
          for (const name of names) {
            const target = join(examplesDirectory, name)
            const proc = Bun.spawn([...UV_FLAGS, ENTRYPOINT, target], {
              cwd: root,
              stdin: "ignore",
              stdout: "pipe",
              stderr: "pipe",
            })

            const [stdout, , exitCode] = await Promise.all([
              new Response(proc.stdout).text(),
              new Response(proc.stderr).text(),
              proc.exited,
            ])

            examples.push({
              name,
              exitCode,
              firstLine: stdout.split("\n", 1)[0] ?? "",
            })
          }

          const result = { examples }
          return {
            content: JSON.stringify(result, null, 2),
            output: result,
            metadata: result,
          }
        },
      })
    })
  },
})
