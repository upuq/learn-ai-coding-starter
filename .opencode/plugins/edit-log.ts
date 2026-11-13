import { appendFile, mkdir } from "node:fs/promises"
import { join } from "node:path"
import { Plugin } from "@opencode/plugin"

const LOGGED_TOOLS = new Set(["edit", "write", "patch"])

export default Plugin.define({
  id: "edit-log",
  async setup(ctx) {
    const logsDirectory = join(ctx.location.directory, "logs")
    const logPath = join(logsDirectory, "plugin-tools.log")

    // Serialize appends so concurrent tool completions do not interleave lines.
    let queue = Promise.resolve()

    const record = async (entry: Record<string, unknown>) => {
      await mkdir(logsDirectory, { recursive: true })
      await appendFile(logPath, `${JSON.stringify(entry)}\n`)
    }

    await ctx.tool.hook("execute.after", (event) => {
      if (event.status !== "completed") return
      if (!LOGGED_TOOLS.has(event.tool)) return

      const entry = { status: event.status, tool: event.tool, input: event.input }
      queue = queue.then(
        () => record(entry),
        () => record(entry),
      )
      return queue
    })
  },
})
