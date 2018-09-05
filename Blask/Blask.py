from flask import Flask, render_template,request
from Blask.blogrenderer import BlogRenderer
from Blask.errors import PageNotExistError
import math
import os


class Blask:
    """
    Blask Main Class.
    :Author: Zerasul <suarez.garcia.victor@gmail.com>
    date: 2018-05-05
    """
    settings = {}
    app = None
    blogrenderer = None

    def __init__(self, **kwargs):
        self.settings['templateDir'] = kwargs['templateDir']
        self.settings['postDir'] = kwargs['postDir']
        self.settings['defaultLayout'] = kwargs['defaultLayout']
        self.settings['staticDir'] = kwargs['staticDir']
        self.settings['tittle'] = kwargs['tittle']
        self.blogrenderer = BlogRenderer(self.settings['postDir'])
        self.app = Flask(__name__, template_folder=self.settings['templateDir'], static_folder=self.settings['staticDir'])
        self.app.add_url_rule('/', endpoint='index', view_func=self._index, methods=['GET'])
        self.app.add_url_rule('/<filename>', view_func=self._getpage, methods=['GET'])
        self.app.add_url_rule('/tag/<tag>', view_func=self._gettag, methods=['GET'])
        self.app.add_url_rule('/search', view_func=self.searchpages, methods=['POST'])
        self.app.add_url_rule('/category/<category>', view_func=self._getcategory, methods=['GET'])
        self.app.add_url_rule('/author/<author>', view_func=self._getauthor, methods=['GET'])
        self.app.add_url_rule('/test', view_func=self._test, methods=['GET'])

    @staticmethod
    def _test404():
        return render_template("404.html")

    def _test(self):
        return render_template("test.html")

    def _index(self):
        """
        Render the Index page
        :return: rendered Index Page
        """
        if request.args.get('page') is not None:
            page = request.args.get('page')
            if type(page) == str:
                page = eval(page)
        else:
            page = 1

        files, page_num = self.blogrenderer.get_recent_five_post(page)
        entries = self.blogrenderer.renderfile("info", abstract=True)

        entries = self.blogrenderer.generate_abstract(entries, files)

        template = 'home.html'

        pages = list(range(1, page_num+1))
        entries.pages = pages
        entries.active_page = page
        entries.tags = self.blogrenderer.get_info("tags")
        entries.toc = None
        return render_template(template, tittle=self.settings['tittle'], **entries.__dict__)

    def _getpage(self, filename):
        """
        Render a blog post
        :param filename: Name of the Blog Post.
        :return: rendered Blog post or 404 page.
        """
        try:
            entry = self.blogrenderer.renderfile(filename)
        except PageNotExistError:
            return render_template("404.html")

        template = entry.template
        if template is None:
            template = self.settings['defaultLayout']
        print(entry.toc)
        return render_template(template, tittle=self.settings['tittle'], **entry.__dict__)

    def _gettag(self, tag):
        """
        Render the Tags Page.
        :param tag: Tag for search
        :return: Rendered tags search.
        """
        postlist = self.blogrenderer.list_posts([tag])
        content = self.blogrenderer.generatetagpage(postlist)
        return render_template(self.settings['defaultLayout'], tittle=self.settings['tittle'], content=content)

    def searchpages(self):
        """
        Render the search page. Must Be on Method POST
        :return: rendered search Page
        """
        postlist = self.blogrenderer.list_posts(search=request.form['search'])
        content = self.blogrenderer.generatetagpage(postlist)
        return render_template(self.settings['defaultLayout'], tittle=self.settings['tittle'], content=content)

    def _getcategory(self, category):
        """
        Render a category searchpage
        :param category:
        :return: rendered category search page
        """
        postlist = self.blogrenderer.list_posts(category=category)
        content = self.blogrenderer.generatetagpage(postlist)
        return render_template(self.settings['defaultLayout'], tittle=self.settings['tittle'], content=content)

    def _getauthor(self, author):
        """
        Render an author searchpage
        :param author: author parameter
        :return:  rendered author search page
        """
        postlist = self.blogrenderer.list_posts(author=author)
        content = self.blogrenderer.generatetagpage(postlist)
        return render_template(self.settings['defaultLayout'], tittle=self.settings['tittle'], content=content)

    def run(self, host, port):
        print(self.app.url_map)
        self.app.run(host=host, port=port)