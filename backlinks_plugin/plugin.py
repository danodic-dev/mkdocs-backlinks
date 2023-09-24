import logging
import os
from dataclasses import dataclass
from typing import List, Dict, Sequence, Any, Optional

from bs4 import BeautifulSoup
from mkdocs.config.base import Config
from mkdocs.config.config_options import ListOfItems, Type
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File, Files
from mkdocs.structure.pages import Page


@dataclass
class Backlink:
    label: str
    destination: str


class LinkScraper:

    def __init__(self, html: str):
        self.html = html

    def links(self):
        """
        Scrapes the valid links from an HTML file. A valid link will not be a
        named anchor and will not point to an external page.
        :return: a list of valid links.
        """
        links = BeautifulSoup(self.html, feature='lxml').find_all('a')
        return self.__remove_invalid_links(links)

    def __remove_invalid_links(self, links):
        return [link for link in links if self.__has_href(link) and self.__is_valid_href(link.attrs['href'])]

    def __is_valid_href(self, href: str) -> bool:
        return not self.__is_named_anchor(href) and not self.__is_external_link(href)

    def __has_href(self, link) -> bool:
        return 'href' in link.attrs

    def __is_named_anchor(self, href: str) -> bool:
        return href.strip().startswith('#')

    def __is_external_link(self, href: str) -> bool:
        return href.strip().lower().startswith('http')


class BacklinksPluginConfig(Config):
    ignored_pages = ListOfItems(Type(str), default=[])


class BacklinksPlugin(BasePlugin[BacklinksPluginConfig]):
    BACKLINKS_DICT_ENTRY_NAME = "backlinks"

    def __init__(self):
        super().__init__()
        self.files_dict = {}

    def on_pre_build(self, *, config: MkDocsConfig) -> None:
        logging.info(f"Excluded pages for backlinking: {self.config.ignored_pages}")

    def on_files(self, files: Files, *, config: MkDocsConfig) -> Optional[Files]:
        self.files_dict = self.__create_file_dict(files.documentation_pages())
        return files

    def on_page_content(self, html, page, config, files):
        for link in LinkScraper(html).links():
            href = link.attrs["href"]
            destination_link = self.__normalize_link(href, page.url)
            if destination_link in self.files_dict:
                file = self.files_dict[destination_link]
                self.__patch_backlinks(file, page)

        return html

    def __patch_backlinks(self, obj: Any, page):
        """
        Will monkey-patch a list of backlinks in the object provided, and will
        add the page provided inside this list of backlinks. The page will
        not be linked to in case it has been excluded in the configurations.
        :param obj: an object to be monkey patched with a list of backlinks.
        :param page: the page to be linked to.
        :return: None.
        """
        if not self.__has_backlinks(obj):
            obj.backlinks = []

        if page in obj.backlinks or self.__is_excluded(page):
            return

        obj.backlinks.append(page)

    def __is_excluded(self, page: Page) -> bool:
        """
        Checks is a page has been excluded in the configuration.
        :param page: the page to be checked for.
        :return: wheter the name of the page provided has been found inside
        the list of ignored pages.
        """
        return page.title in self.config.ignored_pages

    def __has_backlinks(self, obj: Any) -> bool:
        """
        Checks if an object has been monkey-patched with the backlinks list.
        :param obj: the object to be checked for the monkey-patching.
        :return: wheter the object has been monkey-patched or not.
        """
        return hasattr(obj, self.BACKLINKS_DICT_ENTRY_NAME)

    def __normalize_link(self, href: str, page_url: str) -> str:
        """
        Normalizes a link. That means:
        - Checking if links are relative or absolute.
        - Resolving their paths and normalizing them, making sure that the URLs
          are going to be valid when added to the HTML.
        - Normalization will be different, depending on the link being relative
          or absolute.
        :param href: the url scraped from the html file.
        :param page_url: the URL of the page that is linking to the href.
        :return: the normalized URL.
        """
        if self.__is_absolute_link(href):
            return self.__normalize_absolute_link(href)
        return self.__normalize_relative_link(href, page_url)

    def __normalize_relative_link(self, href: str, page_url: str) -> str:
        link = os.path.join(page_url, href)
        return os.path.normpath(link) + "/"

    def __normalize_absolute_link(self, href: str) -> str:
        link = os.path.normpath(href) + "/"
        if link.startswith("/"):
            return link[1:]
        return link

    def __is_absolute_link(self, href: str):
        return href.startswith("/")

    def __create_file_dict(self, files: Sequence[File]) -> Dict[str, Sequence[File]]:
        """
        Creates a dictionary based on the list of files provided as arguments.
        This is used for quickly fetching a page based on its URL.
        :param files: the list of files parsed by mkdocs.
        :return: a dictionary in which the keys are the file paths and value is
                 the file object itself.
        """
        return {file.url: file for file in files}

    def on_page_context(self, context, page, config, nav):
        files = context["pages"]
        self.__assign_backlinks_to_page_context(page.url, files, context)
        return context

    def __assign_backlinks_to_page_context(self,
                                           url: str,
                                           files: List,
                                           context: Dict):
        """
        Mutates the jinja context provided as argument by adding the backlinks
        to it. Backlinks are only added in case a corresponding file for the
        url provided is found *and* this file has a backlinks attribute that
        must have been injected into the file in the previous step.
        :param url: the url of the page for the backlinks to be added to.
        :param files: the list of files that have been monkey-patched with the
                      backlinks at a previous tep.
        :param context: the jinja context that will carry the variables.
        """
        for file in files:
            if file.url == url:
                if hasattr(file, self.BACKLINKS_DICT_ENTRY_NAME):
                    context[self.BACKLINKS_DICT_ENTRY_NAME] = file.backlinks
                return
