# Financial News RSS Feed Flask Application

Welcome to the Fiancial News RSS Feed Flask Application! This simple web application displays the most recent financial news headlines from an RSS feed and allows users to add comments to each item.

### Features
* **RSS Feed Integration:** Fetch and display the latest financial news headlines from an RSS feed.
* **User Comments:** Allow users to leave comments on each news headline.

### Requirements
* Python 3.7+
* Flask
* Feedparser (for parsing RSS feeds)
* SQLite (for storing user comments)
* Dockerfile (for containerization)
* Prometheus Server (for running metrics)

### Installation

1. **Clone the Repository**
``git clone https://github.com/mihaistate/Flask_app.git``
``cd Flask_app``

2. **Set up a Virtual Environment**
``python -m venv venv``
``.\venv\Scripts\Activate.ps1``

3. **Install Dependencies**
``pip install -r requirements.txt``

4. **Create the Database**
``python init_db.py``

### Usage

1. **Run Docker container with Prometheus**
``docker run -p 9090:9090 -v prometheus.yml prom/prometheus``

2. Run the app
``flask run``

3. **Visit the Application**
Open your web browser and go to `http://127.0.0.1:5000` to see the financial news headlines.

### Adding User Comments
Users can add comments to news headlines by:
1. **Selecting a News Item:** Click on 'Comment' underneath headline
2. **Adding a Comment:** Submit comment using the provided form.

### Comment Submission
The comment form requires:
* **Name:** Your name or a pseudonym.
* **Comment:** The content of your comment.

Once submitted, comments are stored in tthe SQLite database and displayed below the respective news item.

### Directory Structure
* `venv` - Contains main application code.
    * `app.py` - Main Python script
    * `__init__.py` - Initializes Flask application.
    * `init_db.py` - Creates database
    * `requirements.txt` - List of Python dependencies
    * `Dockerfile` - For containerizing the application
    * `prometheus.yml` - For running metrics
* `templates/` - HTML templates for rendering pages.
* `static/` - Static files like CSS
* `tests/` - test.py - for unit and integration testing
* `k8s` - for deploying on a Kubernetes cluster

### Warnings
Kubernetes cluster currently does not work. We are working on this issue!
![image](https://github.com/user-attachments/assets/e0e68965-94e7-4c4d-9122-56bf77f58ead)


### Contributing
Feel free to open issues or submit pull requests if you have improvements or bug fixes.

### Contact
For any questions or feedback, please contact mihaistate or open an issue on the GitHub repository.

## Project Contributors
1. **Mihai State (Owner)** - Writing Flask application, database, deploying to Kubernetes cluster on Azure instance, creating database with SQL.
2. **Jon Corales** - Writing Dockerfile, connecting Prometheus server (with help from Domonkos), displaying metrics to Grafana dashboard, creating group presentation.
3. **Domonkos Revesz** - Unit testing, implementing RSS feed, setting up Prometheus server to connect to Flask application.
