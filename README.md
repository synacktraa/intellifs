<div align="center">
  <img src="https://github.com/synacktraa/synacktraa/assets/91981716/901ac9c8-01cb-46d8-bf52-345a46331b8a" alt="ifs-logo-GIF">
  <p>Content-Aware File System.</p>
</div>


## Installation

```shell
pip install intellifs
```
> Note: intellifs only indexes plain text files, HTML, XML and PDF soures by default.

- Add support for all document types
  ```shell
  pip install "unstructured[all-docs]"
  ```

> Refer [unstructured installation documentation](https://unstructured-io.github.io/unstructured/installation/full_installation.html) for more control over document types.

## CLI Usage

Display help section
```shell
ifs
```
```
Usage: ifs COMMAND

Content-Aware File System.

╭─ Commands ─────────────────────────────────────────────╮
│ embedder  Default embedder.                            │
│ index     Index a file or directory.                   │
│ search    Perform semantic search in a directory.      │
│ version   Display application version.                 │
╰────────────────────────────────────────────────────────╯
╭─ Parameters ───────────────────────────────────────────╮
│ help,-h  Display this message and exit.                │
╰────────────────────────────────────────────────────────╯
```

`index` command
```shell
ifs index help
```
```
Usage: ifs index [ARGS]

Index a file or directory.

╭─ Arguments ──────────────────────────────────────────╮
│ *  PATH  Path to file or directory. [required]       │
╰──────────────────────────────────────────────────────╯
```

- Indexing a file.
  ```shell
  ifs index ./Cyber.pdf
  ```
  ![ifs-index-file-GIF](https://github.com/synacktraa/synacktraa/assets/91981716/77d15095-847a-457b-82da-73780a2e1b28)

- Indexing a directory.
  ```shell
  ifs index ./test_docs
  ```
  ![ifs-index-directory-GIF](https://github.com/synacktraa/synacktraa/assets/91981716/36690bcc-9e2a-4162-ba4a-992875b90363)

`search` command
```shell
ifs search help
```
```
Usage: ifs search [ARGS] [OPTIONS]

Perform semantic search in a directory.

╭─ Arguments ───────────────────────────────────────────────────────────╮
│ DIR  Start search directory path. [default: /home/synacktra]          │
╰───────────────────────────────────────────────────────────────────────╯
╭─ Parameters ──────────────────────────────────────────────────────────╮
│ *  --query        -q  Search query string. [required]                 │
│    --max-results  -k  Maximum result count. [default: 5]              │
│    --threshold    -t  Minimum filtering threshold value.              │
│    --return       -r  Component to return. [choices: path,context]    │
╰───────────────────────────────────────────────────────────────────────╯
```

- Search in current directory
  ```shell
  ifs search --query "How does intellifs work?"
  ```

- Search in specific directory
  ```shell
  ifs search path/to/directory --query "How does intellifs work?"
  ```

- Get specific amount of results
  ```shell
  ifs search -q "How does intellifs work?" -k 8
  ```

- Control threshold value for better results
  ```shell
  ifs search -q "How does intellifs work?" -t 0.5
  ```

- Get specific component of results `[default: path mapped contexts JsON]`
  ```shell
  ifs search -q "How does intellifs work?" -r path
  ```

`embedder` command

```shell
ifs embedder help
```
```
Usage: ifs embedder [OPTIONS]

Default embedder.

╭─ Parameters ────────────────────────────────────╮
│ --select  -s  Select from available embedders.  │
╰─────────────────────────────────────────────────╯
```

- Display default embedder
  ```shell
  ifs embedder
  ```
  ```
  {
    "model": "BAAI/bge-small-en-v1.5",
    "dim": 384,
    "description": "Fast and Default English model",
    "size_in_GB": 0.13
  }
  ```
- Select from available embedders
  > Uses https://github.com/synacktraa/minifzf for selection.
  ```shell
  ifs embedder --select
  ```
  ![ifs-embedder-select-GIF](https://github.com/synacktraa/synacktraa/assets/91981716/48512a92-c6e4-4438-b0f3-5a3cc0960d0b)

#### `shell` command
> Starts an interactive shell.

https://github.com/synacktraa/synacktraa/assets/91981716/b746ccf8-e27b-4abd-99cf-528677fb0ef8

## Library Usage

#### Initialize `FileSystem`

```python
from intellifs import FileSystem
ifs = FileSystem()
```

> By default it uses default embedder. You can specify a different `Embedder` instance too.

```python
from intellifs.embedder import Embedder
ifs = FileSystem(
  embedder=Embedder(model="<model-name>", dim=<model-dimension>)
)
```
> Use `Embedder.available_models` to list supported models.

#### `index` method

- Indexing a file
  ```python
  from intellifs.indexables import File
  ifs.index(File(__file__))
  ```

- Indexing a directory
  ```python
  from intellifs.indexables import Directory
  ifs.index(Directory('path/to/directory'))
  ```

#### `is_indexed` method

> Verify If a `File` or `Directory` has been indexed.
```python
file = File(__file__)
ifs.is_indexed(file)
ifs.is_indexed(file.directory)
```

#### `search` method

- Search in current directory
  ```python
  ifs.search(query="How does intellifs work?")
  ```

- Search in specific directory
  ```python
  ifs.search(
    directory=Directory('path/to/directory'),
    query="How does intellifs work?"
  )
  ```

- Get specific amount of results
  ```python
  ifs.search(query="How does intellifs work?", max_results=8)
  ```

- Control threshold value for better results
  ```python
  ifs.search(
    query="How does intellifs work?", score_threshold=0.5
  )
  ```


# How It Works?

The `FileSystem` is a sophisticated file system management tool designed for organizing and searching through files and directories based on their content. It utilizes embeddings to represent file contents, allowing for semantic search capabilities. Here's a breakdown of its core components and functionalities:

### Core Components

#### `Metadata` and `Index`
- **Metadata**: A structured representation that includes file contexts (chunks of text extracted from files), the directory path, filepath, and the last modified timestamp.
- **Index**: Consists of embeddings (vector representations of file contents) and associated metadata.

#### `FileSystem` Class
The `FileSystem` class is the heart of the system, integrating various components to facilitate file indexing, searching, and management.

### Initialization

Upon initialization, the `FileSystem` prepares the environment for indexing and searching files and directories with the following steps:

- **Embedder Setup**: An embedder is initialized to generate vector embeddings from file content. If a custom embedder is not provided, the system defaults to a pre-configured option suitable for general-purpose text embedding.

- **Local Storage Initialization**: The system sets up a local storage mechanism to cache the embeddings and metadata. This involves:
  - Determining the storage path based on the embedder's name, ensuring a unique cache directory for different embedders.
  - Creating a mapping file (`map.json`) within the cache directory to maintain a record of collection names associated with base paths.

- **Base Path Handling**: The FileSystem intelligently handles base paths to accommodate the file system structure of different operating systems. 
  - **Windows Systems**: On Windows, base paths are recognized as drive letters (e.g., `C:`, `D:`). This allows the system to manage files and directories across different drives distinctly.
  - **POSIX Systems**: For POSIX-compliant systems (like Linux and macOS), base paths are identified as root directories (e.g., `/var`, `/home`). This approach facilitates indexing and searching files in a structured manner consistent with UNIX-like directory hierarchies.

- **Collection Management**: Utilizes a local persistent vector database, managed through the `qdrant_client`, to store and retrieve embeddings and metadata.

### Indexing Files and Directories
- **File Indexing**: Generates an index for a single file by extracting text, partitioning it into manageable chunks, and converting these chunks into embeddings. Metadata is also generated to include the file's contextual information and modification timestamp.
- **Directory Indexing**: Recursively indexes all files within a directory. It checks for modifications to ensure the index is current, adds new files, and removes entries for deleted files.

### Searching
Allows for semantic search within specified directories or globally across all indexed files. Searches are performed using query embeddings to find the most relevant files based on their content embeddings.

### Workflow
1. **Generate Index**: When a file or directory is indexed, the system extracts text, generates embeddings, and stores this information along with metadata in a dedicated collection.
2. **Search**: Input a text query to search across indexed files and directories. The system converts the query into an embedding and retrieves the most relevant files based on cosine similarity.
3. **Management**: The system supports adding, updating, and deleting files or directories in the index to keep the database current with the filesystem.