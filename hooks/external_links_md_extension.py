from typing import List
from urllib.parse import urlparse

import markdown
from mkdocs.config.defaults import MkDocsConfig


class ExternalLinksTreeProcessor(markdown.treeprocessors.Treeprocessor):
    """
    Adds target="_blank" and rel="noopener" to external links.
    """

    def __init__(self, md, ignore_domains: List[str]):
        super().__init__(md)
        # convert to set for faster lookup
        self.ignore_domains = set(ignore_domains)

    def run(self, root):
        for element in root.iter():
            if element.tag == "a":
                href = element.get("href", "")

                # parse the href and check if it's an absolute URL with http or https scheme
                parsed_url = urlparse(href)

                if parsed_url.scheme in ["http", "https"]:
                    # remove port, if present
                    domain = parsed_url.netloc.split(":")[0]

                    # skip if the domain is in the ignore list
                    if domain in self.ignore_domains:
                        continue

                    element.set("target", "_blank")
                    element.set("rel", "noopener")


class ExternalLinksExtension(markdown.Extension):
    def __init__(self, **kwargs):
        self.config = {
            "ignore_domains": [[], "List of domains to ignore"],
        }
        super(ExternalLinksExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md: markdown.Markdown):
        ignore_domains = self.getConfig("ignore_domains", [])
        if not isinstance(ignore_domains, list):
            raise ValueError("'ignore_domains' config must be a list")

        md.treeprocessors.register(
            ExternalLinksTreeProcessor(md, ignore_domains), "external_links", -1000
        )


def on_config(config: MkDocsConfig, **kwargs):
    # a list of domains to ignore
    # WARNING: requires re-running `mkdocs serve` when changed
    IGNORE_DOMAINS = ["example.com"]

    # inject the markdown extension
    config.markdown_extensions.append(
        ExternalLinksExtension(ignore_domains=IGNORE_DOMAINS)
    )
    return config
