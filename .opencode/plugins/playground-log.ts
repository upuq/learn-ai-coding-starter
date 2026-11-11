import { appendFile, mkdir } from "node:fs/promises"
import { join } from "node:path"
import { Plugin } from "@opencode/plugin"

const LOG_LINE = "playground shell request\n"

export default Plugin.define({
  id: "playground-log",
  async setup(ctx) {
    const logsDirectory = join(ctx.location.directory, "logs")
    const logPath = join(logsDirectory, "plugin-playground.log")

    await ctx.shell.hook("create.before", async (event) => {
      if (!event.command.includes("playground/server.py")) return
      await mkdir(logsDirectory, { recursive: true })
      await appendFile(logPath, LOG_LINE)
    })
  },
})
