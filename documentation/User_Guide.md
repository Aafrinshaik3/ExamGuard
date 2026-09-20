ExamGuard - User Guide

1. Introduction

This guide explains how students and administrators interact with the ExamGuard platform.

ExamGuard provides an online examination environment combined with automated monitoring and integrity analytics.

The system has two primary user roles:

* Student
* Administrator

⸻

2. Starting ExamGuard

Start the application using:

python3 -c "from app import create_app; create_app().run(host='0.0.0.0', port=5001, debug=True)"

On Windows:

python -c "from app import create_app; create_app().run(host='0.0.0.0', port=5001, debug=True)"

Open the application in a browser:

http://localhost:5001

⸻

3. Student Workflow

Step 1 - Open the Student Interface

Access the student interface using the student route configured in the application.

For the current ExamGuard route:

http://localhost:5001/student

⸻

Step 2 - Student Authentication

The student provides the required login information.

The authentication system verifies the submitted credentials before allowing access to the examination functionality.

After successful authentication, the student can access the available examination functionality.

⸻

Step 3 - Prepare for the Examination

Before starting the examination, the student should:

* Ensure the webcam is connected.
* Ensure the microphone is available if audio monitoring is enabled.
* Allow the required browser permissions.
* Ensure the camera provides a clear view.
* Remain in the examination environment during the examination.

⸻

Step 4 - Start the Examination

The student starts the assigned examination through the examination interface.

Once the examination begins, configured monitoring mechanisms can begin collecting examination-related events.

⸻

4. Examination Monitoring

ExamGuard can monitor multiple types of events.

4.1 Face Monitoring

The webcam is used for computer-vision-based face monitoring.

The system can identify whether the expected face is visible.

⸻

4.2 Face Absence

If the expected face is not detected for the configured monitoring period, a face-absence event can be recorded.

The configured face-absence threshold is:

60 seconds

⸻

4.3 Multiple Face Detection

The system can detect when more than one face is present in the camera view.

The configured multiple-face threshold is:

1

The resulting event contributes to the violation analysis.

⸻

4.4 Tab Switching

ExamGuard can monitor browser tab-switch events during the examination.

A tab-switch event has a configured violation weight of:

8 points

⸻

4.5 Browser Focus Loss

The system can detect when the examination browser window loses focus.

The configured violation weight for a focus-loss event is:

5 points

⸻

4.6 Audio Monitoring

ExamGuard includes configured audio monitoring for identifying audio-spike events.

An audio-spike event has a configured violation weight of:

6 points

Environmental noise and microphone conditions can affect audio monitoring.

⸻

5. Examination Integrity Analysis

ExamGuard assigns predefined weights to configured monitoring events.

Event	Weight
Tab Switch	8
Focus Loss	5
Face Absent	10
Multiple Face	15
Audio Spike	6
Face Mismatch	12

The accumulated monitoring information is used for examination integrity analysis.

The integrity analysis considers the configured events and thresholds rather than relying on one individual event.

⸻

6. Examination Submission

The student completes the examination questions through the provided interface.

After completing the examination, the student submits the examination using the available submission functionality.

The submitted examination information can then be processed by the application.

⸻

7. Administrator Workflow

Step 1 - Open the Administrator Interface

Access the administrator interface:

http://localhost:5001/admin

⸻

Step 2 - Administrator Authentication

The administrator provides the required credentials.

After successful authentication, the administrator can access the administrative functionality provided by ExamGuard.

⸻

Step 3 - Review Examination Information

The administrator can review available examination-related information through the administrative interface.

This may include:

* Student information.
* Examination information.
* Examination results.
* Monitoring information.
* Violation information.

⸻

8. Reviewing Monitoring Events

Administrators can review the monitoring events recorded during examinations.

These can include:

* Face absence.
* Multiple faces.
* Tab switching.
* Browser focus loss.
* Audio spikes.
* Face mismatch, where configured.

The events provide additional context for reviewing examination integrity.

⸻

9. Integrity Analytics

The administrator can review the integrity information calculated from the recorded monitoring events.

The analysis uses the configured violation weights and thresholds.

The configured maximum values include:

Parameter	Value
Maximum Violations	5
Maximum Face Absence Events	5
Maximum Tab Switches	5

These values are configuration parameters of the current implementation.

⸻

10. Report Generation

ExamGuard includes a report-generation component using the project’s LangChain-based processing.

The purpose of the report is to convert collected examination and integrity information into a structured narrative that can assist the administrator in reviewing the examination.

The generated report should be considered together with the underlying examination and monitoring information.

⸻

11. Responsible Interpretation of Monitoring Results

Automated monitoring can be affected by environmental and technical conditions.

For example:

* Poor lighting can affect face detection.
* Camera positioning can affect face visibility.
* Background noise can affect audio monitoring.
* Browser behavior can affect browser-event detection.
* Temporary technical problems can produce unexpected monitoring events.

Therefore, monitoring events should be reviewed in context rather than treated as standalone proof of examination misconduct.

⸻

12. Basic Student Checklist

Before starting an examination, students should ensure:

* Webcam is connected.
* Microphone is available if required.
* Browser permissions are enabled.
* Camera view is clear.
* Internet connection is stable.
* Examination page is accessible.
* Required authentication information is available.

⸻

13. Basic Administrator Checklist

Administrators should verify:

* Administrator login works.
* Examination information is available.
* Student information is available.
* Monitoring events are recorded.
* Violation information is available.
* Integrity analysis is accessible.
* Reports can be generated where configured.

⸻

14. Ending the Application

After completing testing or demonstration, stop the Flask server from the terminal using:

Ctrl + C

Deactivate the Python virtual environment:

deactivate

⸻

15. Summary

ExamGuard provides an integrated workflow for online examinations and automated monitoring.

The student completes an examination while configured monitoring mechanisms collect examination-related events. These events are processed using predefined weights and thresholds. Administrators can then review examination information, monitoring events, integrity analytics, and generated reports.