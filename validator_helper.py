import subprocess

def exec_prog(*args, **kwargs):
    """
    Wrap subprocess.run to capture output as text
    """
    exec_args = {**kwargs, "capture_output": True, "text": True}
    return subprocess.run(*args, **exec_args)
