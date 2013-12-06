# https://github.com/daGrevis/mdx_linkify | MIT License

import bleach

from html5lib.sanitizer import HTMLSanitizer

from markdown.postprocessors import Postprocessor
from markdown import Extension


class MyTokenizer(HTMLSanitizer):
    def sanitize_token(self, token):
        return token


class LinkifyPostprocessor(Postprocessor):
    def run(self, text):
        text = bleach.linkify(text, callbacks=[], tokenizer=MyTokenizer)
        return text


class LinkifyExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.postprocessors.add("linkify", LinkifyPostprocessor(md), "_begin")


def makeExtension(configs=None):
    return LinkifyExtension(configs=configs)