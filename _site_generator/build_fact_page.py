import markdown
import string
import textwrap

def fact_page_url(fact_dict):
    if fact_dict['quantity unit'] == '':
        url = '{verb} how many {thing} {time unit}'.format(**fact_dict)
    else:
        url = '{verb} how many {quantity unit} of {thing} {time unit}'.format(**fact_dict)
    url = url.translate(str.maketrans('', '', string.punctuation))  # remove punctuation
    url = ' '.join(url.split())  # remove excess whitespace
    url = url.replace(' ','-')  # replace spaces with hyphens
    url = url + '.html'  # add HTML extension
    return url

def fact_page_fact(fact_dict):
    if fact_dict['quantity unit'] == '':
        fact_string = '{verb} {per capita} {thing} {time unit}'.format(**fact_dict)
    else:
        fact_string = '{verb} {per capita} {quantity unit} of {thing} {time unit}'.format(**fact_dict)
    fact_string = ' '.join(fact_string.split())  # remove excess whitespace
    return fact_string

def fact_page_html(url='', fact='', source='', note='', url_list=[], start_page=False, about_page=False, **kwargs):
    # check that inputs are correct types
    if not isinstance(url, str):
        raise TypeError('url needs to be a string')
    if not isinstance(fact, str):
        raise TypeError('fact needs to be a string')
    if not isinstance(source, str):
        raise TypeError('source needs to be a string')
    if not isinstance(note, str):
        raise TypeError('note needs to be a string')
    if not isinstance(url_list, list):
        raise TypeError('url_list needs to be a list of strings')
    if not isinstance(start_page, bool):
        raise TypeError('start_page needs to be True or False')

    # check that required arguments are present
    if not url:
        raise ValueError('url is required')
    if not url_list:
        raise ValueError('url_list is required')

    # compute intermediate html chunks
    if source:
        source_html = f'<div><h2>Source:</h2> {markdown.markdown(source)}</div>'
    else:
        source_html = ''

    if note:
        note_html = f'<div><h2>Note:</h2> {markdown.markdown(note)}</div>'
    else:
        note_html = ''

    title = f'The average human being {fact}'

    if start_page:
        start_page_script = f"""\
            <script>
                var urls = {url_list};
                location.href = urls[Math.floor(Math.random() * urls.length)];
            </script>
            """
        start_page_script = textwrap.dedent(start_page_script)
    else:
        start_page_script = ''

    if about_page:
        fact_string = 'made 0.00000003% of this website'
        with open('about.md', 'r') as about_file:
            about_text = about_file.read()
        about_text = f'<article>\n{markdown.markdown(about_text)}\n</article>'
    else:
        about_text = ''
        fact_string = None

    # load template
    with open('fact_page_template.html', 'r') as fact_page_template_file:
        fact_page_template_string = fact_page_template_file.read()

    # return completed template
    fact_string = fact_string if fact_string else fact
    return fact_page_template_string.format(
        url=url, 
        fact=fact_string, 
        title=title, 
        source_html=source_html, 
        note_html=note_html, 
        url_list=url_list,
        start_page_script=start_page_script,
        about_text=about_text
        )