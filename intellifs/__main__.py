"""IntelliFS CLI Integration."""

import json
from pathlib import Path
from typing import Annotated, Literal

from cyclopts import App, Parameter, validators

app = App(
    name='ifs',
    help="Content-Aware File System.",
    version_flags=['version'], 
    help_flags=['help', '-h'])

app['help'].group = app.group_parameters

cached_fs = {'instance': None}

def get_fs():
    if cached_fs.get('instance') is None:
        from . import FileSystem
        cached_fs['instance'] = FileSystem()
    return cached_fs['instance']

def print_json(__input: list | dict):
    print(json.dumps(__input, indent=4))

@app.command(name='index')
def index(path: Annotated[Path, Parameter(validator=validators.Path(exists=True))], /):
    """
    Index a file or directory.
    
    @param path: Path to file or directory.
    """

    from .indexables import File, Directory
    if path.is_file():
        target = File(path)
    elif path.is_dir():
        target = Directory(path)
    else:
        print(f"Only file and directory can be indexed.")
        return
    
    get_fs().index(target)


@app.command(name='search')
def search(
    dir: Annotated[Path, Parameter(
        validator=validators.Path(exists=True, file_okay=False))] = Path.cwd(), 
    /, 
    *, 
    query: Annotated[str, Parameter(name=('-q', '--query'))],
    max_results: Annotated[int, Parameter(name=('-k', '--max-results'))] = 5,
    threshold: Annotated[float, Parameter(
        name=('-t', '--threshold'), validator=validators.Number(gte=0.0, lte=1.0))] = None,
    _return: Annotated[Literal['path', 'context'], Parameter(name=('-r', '--return'))] = None,
):
    """
    Perform semantic search in a directory.

    @param dir: Start search directory path.
    @param query: Search query string.
    @param max_results: Maximum result count.
    @param threshold: Minimum filtering threshold value.
    @param _return: Component to return.
    """

    from .indexables import Directory
    mapping = get_fs().search(query, Directory(dir), max_results, threshold)
    if mapping:
        if len(mapping) == 1:
            if _return == 'path':
                print(list(mapping)[0])
            elif _return == 'context':
                print_json(list(mapping.values())[0])
            else:
                print_json(mapping)
            return
        
        from minifzf import Selector
        selector = Selector(
            rows=[(filepath,) for filepath in mapping], headers=[query])
        selected = selector.select(disable_print=True)
        if not selected:
            return
        if _return == 'path':
            print(selected)
        elif _return == 'context':
            print_json(mapping[selected])
        else:
            print_json({selected: mapping[selected]})


@app.command(name='embedder')
def embedder(
    *,
    select: Annotated[bool, Parameter(
        name=('-s', '--select'), negative="", show_default=False)] = False
):
    """
    Default embedder.

    @param select: Select from available embedders.
    """
    from . import settings
    if select is False:
        print_json(settings.DEFAULT_EMBEDDER)
        return
    
    from minifzf import Selector #https://github.com/synacktraa/minifzf
    from .embedder import Embedder
    selector = Selector.from_mappings(Embedder.available_models)
    selected = selector.select()
    if not selected:
        return

    settings.DEFAULT_EMBEDDER_FILE.write_text(json.dumps(selected))

@app.command(name='shell')
def shell():
    """Interactive Shell."""
    try:
        app.interactive_shell(prompt='ifs> ', quit=['q', 'quit', 'exit'])
    except KeyboardInterrupt:
        exit(0)

if __name__ == "__main__":
    app()