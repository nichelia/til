from pathlib import Path
from typing import Dict
import time

from jinja2 import Environment, FileSystemLoader


def write_to_file(directory: str, contents: str) -> None:
    """
    Write template output with parsed contents to file.

    Args:
        directory {str} The file directory to write to
        contents {str} The template parsed contents to output
    """
    if not directory or not contents:
        return

    with open(directory, "w") as f:
        f.write(contents)


def fill_template(
    template_directory: str, template_file: str, values = None
) -> str:
    """
    Use Jinja to fill in values given a template

    Args:
        template_directory {str} Directory with all Jinja templates
        template_file {str} Filename of Jinja template in use
        values {dict} Key (matches a Jinja tag), Value pairs to fill in

    Returns:
        {str} Template parsed contents
    """
    if values is None:
        values = {}
    env = Environment(
        loader=FileSystemLoader(template_directory),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(template_file)
    ret = template.render(values)
    return ret


def get_category_name(text: str) -> str:
    """
    Generate a category name.
    Capitalise the first letter of every word.
    Replace any `-` with a space.

    Args:
        text {str} The text value to parse
    
    Returns:
        {str} The parsed text
    """
    return text.title().replace('-', ' ')


def get_category_link(text: str) -> str:
    """
    Generate a category link.
    A markdown link beginning with '#' and
    text split with dash.

    Args:
        text {str} The text value to parse
    
    Returns:
        {str} The parsed text
    """
    return f"#{text.lower().replace(' ', '-')}"


def get_topic_name(text: str) -> str:
    """
    Generate a topic name.
    Capitalise the first letter of every word.
    Replace any `-` with a space.

    Args:
        text {str} The text value to parse
    
    Returns:
        {str} The parsed text
    """
    return text.title().replace('-', ' ')


def get_topic_link(text: str) -> str:
    """
    Generate a topic link.
    A markdown link, text split with dash.

    Args:
        text {str} The text value to parse
    
    Returns:
        {str} The parsed text
    """
    return f"{text.lower().replace(' ', '-')}"


def get_topic_created_datetime(epoch: float) -> str:
    """
    Generate a topic creation datetime.

    Args:
        epoch {float} The epoch timestamp of creation time

    Returns:
        {str} Human readable datetime
    """
    if epoch == 0:
        return None
    return time.strftime("%Y-%m-%d %H:%M (%Z)", time.localtime(epoch))


def get_categories_and_topics(root_directory: str) -> Dict:
    """
    Generate the category/topic data for README.

    Args:
        root_directory {str} The directory that includes the categories/topics
    
    Returns:
        {dict} Data to be used in the template
    """
    ret = {}
    markdown_files = set(Path(root_directory).glob('**/*.md')) - set(Path(root_directory).glob('*.md'))
    files = sorted(markdown_files, reverse=True)

    ret["categories"] = []
    ret["tils"] = len(files)
    category = ""
    topics = []
    while files:
        file = files.pop()
        new_category = str(file.parent)
        if category == "":
            category = new_category
        if new_category != category:
            data = {"name": get_category_name(category),
                    "link": get_category_link(category),
                    "topics": topics}
            ret["categories"].append(data)
            category = new_category
            topics = []
            data = {"name": get_topic_name(str(file.stem)),
                    "link": get_topic_link(str(file)),
                    "createdDateTime": get_topic_created_datetime(getattr(file.stat(), "st_birthtime", 0))}
            topics.append(data)
        else:
            data = {"name": get_topic_name(str(file.stem)),
                    "link": get_topic_link(str(file)),
                    "createdDateTime": get_topic_created_datetime(getattr(file.stat(), "st_birthtime", 0))}
            topics.append(data)
        if len(files) == 0:
            data = {"name": get_category_name(new_category),
                    "link": get_category_link(new_category),
                    "topics": topics}
            ret["categories"].append(data)

    return ret


def run():
    root_directory = "."
    template_file = "README.md.jinja"
    output_directory = "README.md"
    values = get_categories_and_topics(root_directory)
    contents = fill_template(root_directory, template_file, values)
    write_to_file(output_directory, contents)


if __name__ == "__main__":
    run()
