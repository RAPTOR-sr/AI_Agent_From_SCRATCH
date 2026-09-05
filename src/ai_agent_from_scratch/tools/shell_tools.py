import subprocess


def run_command(command):
    """Run a shell command after asking the user for confirmation.

    Args:
        command: Shell command to execute.

    Returns:
        The command output, or a message when execution is declined or empty.

    Raises:
        subprocess.TimeoutExpired: If the command runs longer than 120 seconds.
    """
    answer = input(f"Run '{command}'? [Y/N]: ")

    if answer.strip().lower() != "y":
        return "Action rejected: User explicitly declined to run this command. Do NOT retry or call this command again."

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        timeout=120,
    )

    output = (result.stdout + result.stderr).strip()

    return output or f"No output, exit code {result.returncode}"