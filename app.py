from flask import Flask, render_template, request
from flask_paginate import Pagination, get_page_parameter

app = Flask(__name__)

@app.route('/results')
def results():
    # Generate some example results (in this case, just strings from 'A' to 'Z')
    results = list(map(chr, range(ord('A'), ord('Z')+1)))
    
    # Get the page number from the query parameters
    page_number = request.args.get(get_page_parameter(), type=int, default=1)
    
    # Define the number of results per page
    per_page = 5
    
    # Calculate the start and end indexes of the results to be displayed on the current page
    start_index = (page_number - 1) * per_page
    end_index = start_index + per_page
    
    # Create a Pagination object with the total number of results and the number of results per page
    pagination = Pagination(page=page_number, total=len(results), per_page=per_page)
    
    # Pass the results for the current page and the pagination object to the template
    return render_template('results.html', results=results[start_index:end_index], pagination=pagination, page_parameter=get_page_parameter())

if __name__ == '__main__':
    app.run(debug=True)
