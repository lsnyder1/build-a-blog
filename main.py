#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import os
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape=True)

class Blog(db.Model):
    title=db.StringProperty(required=True)
    created=db.DateTimeProperty(auto_now_add=True)
    content=db.TextProperty(required=True)

class Handler(webapp2.RequestHandler):
    def renderError(self, error_code):
        """ Sends an HTTP error code and a generic "oops!" message to the client. """

        self.error(error_code)
        self.response.write("Oops! Something went wrong.")



class MainPage(Handler):
    def get(self):
        blogs= db.GqlQuery("Select * FROM Blog ORDER BY created DESC LIMIT 5")
        t= jinja_env.get_template("main.html")
        cont=t.render(blogs=blogs)
        self.response.write(cont)





class NewPost(Handler):
    def get(self):

        t= jinja_env.get_template("newpost.html")
        cont=t.render(title=self.request.get("title"),
                      content=self.request.get("content"),
                      error=self.request.get("error"))
        self.response.write(cont)

    def post(self):
        title=self.request.get("title")
        content=self.request.get("content")


        if title and content:
            a=Blog(title=title,content=content)
            a.put()

            self.redirect("/")

        else:

            error="Enter a title and content."
            self.redirect("/newpost?error="+error)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/newpost', NewPost)
], debug=True)
