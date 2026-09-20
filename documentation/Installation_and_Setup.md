ExamGuard - Installation and Setup Guide

1. Project Overview

ExamGuard is a Flask-based online examination monitoring and integrity analytics platform.

The application provides examination functionality along with monitoring features such as face detection, face absence detection, multiple-face detection, browser tab-switch detection, browser focus-loss detection, audio monitoring, violation tracking, and integrity analysis.

⸻

2. System Requirements

The following are required to run ExamGuard:

* Python 3.x
* Git
* Modern web browser
* Webcam for face monitoring features
* Microphone for audio monitoring features
* Internet connection for installing project dependencies
* Sufficient system permissions for camera and microphone access

⸻

3. Clone the Repository

Open Terminal or Command Prompt and clone the GitHub repository:

git clone https://github.com/Aafrinshaik3/ExamGuard.git

Move into the project directory:

cd ExamGuard

⸻

4. Create a Virtual Environment

A virtual environment is recommended so that ExamGuard dependencies remain isolated from other Python projects.

macOS / Linux

python3 -m venv venv

Activate the environment:

source venv/bin/activate

After activation, the terminal should show (venv).

Windows

Create the environment:

python -m venv venv

Activate it:

venv\Scripts\activate

⸻

5. Install Project Dependencies

After activating the virtual environment, install the dependencies listed in requirements.txt:

pip install -r requirements.txt

If pip is not available directly, use:

python3 -m pip install -r requirements.txt

on macOS/Linux, or:

python -m pip install -r requirements.txt

on Windows.

⸻

6. Application Configuration

ExamGuard uses a Flask application factory.

The application is created using:

from app import create_app

The project should be configured according to the configuration files and environment variables included or documented in the repository.

Sensitive information such as:

* Passwords
* API keys
* Secret keys
* Authentication credentials

should not be committed to GitHub.

If the project requires environment variables, configure them locally according to the application’s configuration.

⸻

7. Run the Flask Application

After activating the virtual environment and installing dependencies, start ExamGuard using the project’s application factory:

macOS / Linux

python3 -c "from app import create_app; create_app().run(host='0.0.0.0', port=5001, debug=True)"

Windows

If python3 is not recognized on Windows, use:

python -c "from app import create_app; create_app().run(host='0.0.0.0', port=5001, debug=True)"

The application runs on:

http://localhost:5001

⸻

8. Accessing the Application

After starting the Flask server, open a web browser and navigate to:

http://localhost:5001

The available student and administrator routes depend on the routes configured in the Flask application.

If the current application provides the following routes, they can be accessed through:

Student

http://localhost:5001/student

Administrator

http://localhost:5001/admin

⸻

9. Camera and Microphone Permissions

ExamGuard uses monitoring features that may require access to the computer’s camera and microphone.

When prompted by the browser or operating system:

1. Allow camera access.
2. Allow microphone access.
3. Make sure another application is not exclusively using the camera or microphone.

If permissions were previously denied, open the browser’s site permissions and allow access for the local ExamGuard application.

⸻

10. Monitoring Requirements

For camera-based monitoring:

* A functioning webcam is required.
* The camera should have a clear view of the student.
* Adequate lighting is recommended.
* Only the intended student should normally be visible to the camera.

For audio monitoring:

* A functioning microphone is required.
* The microphone should be accessible to the browser/application.
* Environmental noise can affect audio monitoring.

⸻

11. Running the Application on Windows

Windows users do not need the virtual environment from the developer’s computer.

After cloning the repository, Windows users should create their own environment:

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

Then start the application:

python -c "from app import create_app; create_app().run(host='0.0.0.0', port=5001, debug=True)"

Open:

http://localhost:5001

⸻

12. Troubleshooting

Python is not recognized

Check the installed Python version:

python3 --version

or on Windows:

python --version

Dependencies are missing

Activate the virtual environment and run:

pip install -r requirements.txt

Camera is not detected

Check:

* Camera connection.
* Operating-system camera permissions.
* Browser camera permissions.
* Whether another application is using the camera.

Microphone is not detected

Check:

* Microphone connection.
* Operating-system microphone permissions.
* Browser microphone permissions.
* Whether another application is using the microphone.

Port 5001 is already in use

Stop the application currently using port 5001, or configure ExamGuard to use another available port.

Application does not start

Verify that:

1. You are inside the ExamGuard directory.
2. The virtual environment is activated.
3. Dependencies have been installed.
4. The required configuration is available.
5. The application factory can be imported.

You can test the application import using:

python3 -c "from app import create_app; print('ExamGuard application loaded successfully')"

⸻

13. Successful Installation

A successful installation should allow the Flask application to start without dependency or import errors.

The application should then be accessible through:

http://localhost:5001

The student and administrator functionality can then be accessed through the routes implemented by the application.

⸻

14. Stopping the Application

To stop the Flask development server, return to the terminal where it is running and press:

Ctrl + C

To deactivate the virtual environment:

deactivate