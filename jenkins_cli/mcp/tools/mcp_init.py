from jenkins_cli.commands.init_cmd import init
import sys
import io

async def jenkins_init_tool(job_name=None, debug=False):
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()
    try:
        init.callback(name=job_name, debug=debug)
        output = mystdout.getvalue()
        return {"output": output}
    except Exception as e:
        return {"error": str(e)}
    finally:
        sys.stdout = old_stdout
