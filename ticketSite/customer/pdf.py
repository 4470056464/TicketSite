import os
from io import StringIO, BytesIO
from django.conf import settings
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    # context = Context(context_dict)
    context=context_dict
    html  = template.render(context)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), result,link_callback=fetch_resources,encoding='utf-16')
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
    # return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
def fetch_resources(uri,rel):
    path= os.path.join(settings.MEDIA_ROOT,uri.replace(settings.MEDIA_URL,""))
    return path