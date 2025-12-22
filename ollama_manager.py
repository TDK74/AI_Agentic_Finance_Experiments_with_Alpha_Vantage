import subprocess

from ollama import Client


def model_exists(model_name):
    """Check if a specific Ollama model is available locally.
    Args:
        model_name (str): Name of the model to check.
    Returns:
        bool: True if the model exists, False otherwise.
    """
    client = Client(host = 'http://localhost:11434')
    models = client.list()['models']

    return any(getattr(m, 'model', None) == model_name for m in models)


def list_model_names():
    """List the names of all available Ollama models.
    Returns:
        list[str]: A list of model names.
    """
    client = Client(host = 'http://localhost:11434')
    models = client.list()['models']

    return [m.model for m in models]


def start_model(model_name = "mistral:7b"):
    """Start the Ollama model if not already running.
    Args:
        model_name (str, optional): Name of the model to start. Defaults to "mistral:7b".
    Raises:
        Exception: If there is an error starting the model.
    """
    try:
        # Ollama models are loaded on-demand, so just check if the server is running
        client = Client(host = 'http://localhost:11434')
        client.generate(model = model_name, prompt = "Test")
        print(f"Model {model_name} is ready!")

    except Exception as e:
        print(f"Error starting model {model_name}: {e}")
        raise


def stop_model(model_name: str) -> bool:
    """Stop a running Ollama model via CLI.
    Args:
        model_name (str): Name of the model to stop.
    Returns:
        bool: True if the model was stopped successfully.
    Raises:
        RuntimeError: If there is an error stopping the model.
    """
    try:
        result = subprocess.run(["ollama", "stop", model_name],
                                capture_output = True, text = True, timeout = 10)

        if result.returncode == 0:
            print(f"Model {model_name} stopped successfully.")

            return True

        else:
            raise RuntimeError(result.stderr.strip())

    except Exception as e:
        raise RuntimeError(f"Failed to stop model '{model_name}': {e}") from e


if __name__ == "__main__":
    start_model("phi3.5:3.8b")
    model_exists("gemma2:2b")
    list_model_names()
