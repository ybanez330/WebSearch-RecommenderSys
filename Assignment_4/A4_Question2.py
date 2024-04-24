#-------------------------------------------------------------------------
# AUTHOR: Julia Ybanez
# FILENAME: A4_Question2.py
# SPECIFICATION: Retrieving information from html text using tags
# FOR: CS4250 - Assignment #4
# TIME SPENT: 2 hours
#-----------------------------------------------------------*/


from bs4 import BeautifulSoup

html = """
<html>
<head>
<title>My first web page</title>
</head>
<body>
<h1>My first web page</h1>
<h2>What this is tutorial</h2>
<p>A simple page put together using HTML. <em>I said a simple page.</em>.</p>
<ul>
<li>To learn HTML</li>
<li>
To show off
<ol>
<li>To my boss</li>
<li>To my friends</li>
<li>To my cat</li>
<li>To the little talking duck in my brain</li>
</ol>
</li>
<li>Because I have fallen in love with my computer and want to give her some HTML loving.</li>
</ul>
<h3>Where to find the tutorial</h3>
<p><a href="http://www.aaa.com"><img src=http://www.aaa.com/badge1.gif></a></p>
<h4>Some random table</h4>
<table>
<tr class="tutorial1">
<td>Row 1, cell 1</td>
<td>Row 1, cell 2<img src=http://www.bbb.com/badge2.gif></td>
<td>Row 1, cell 3</td>
</tr>
<tr class="tutorial2">
<td>Row 2, cell 1</td>
<td>Row 2, cell 2</td>
<td>Row 2, cell 3<img src=http://www.ccc.com/badge3.gif></td>
</tr>
</table>
</body>
</html>
"""


# Create a BeautifulSoup object
soup = BeautifulSoup(html, 'html.parser')

# a. The title of the HTML page
print(f"a. Title of the HTML page:",soup.title.text,"\n")


# b. The second list item below 'To show off'
second_li = soup.select_one('li:-soup-contains("To my boss") + li')
print(f"b. Second list item: '{second_li.text}'\n")

# c. All cells of Row 2
row_2_cells = soup.select('.tutorial2 td')
print("c. All cells of Row 2:")
for cell in row_2_cells:
    print(cell.text)

# d. All h2 headings that include the word “tutorial”
h2_with_tutorial = soup.find_all('h2')
print("\nd. All h2 headings with the word 'tutorial':")
for heading in h2_with_tutorial:
    if 'tutorial' in heading.text:
        print(heading.text)

# e. All text that includes the “HTML” word
html_text = soup.find_all(string=lambda text: 'HTML' in text)
print("\ne. All text including the word 'HTML':")
for text in html_text:
    print(text)

# f. All cells’ data from the first row of the table
first_row_cells = soup.select('.tutorial1 td')
print("\nf. All cells' data from the first row of the table:")
for cell in first_row_cells:
    print(cell.text)

# g. All images from the table
print("\ng. All images from the table:")
for img in soup.select('table img'):
    print(img['src'])