# ExamGuard - Project Documentation

## 1. Project Title

**ExamGuard - Online Examination Monitoring and Integrity Analytics Platform**

---

## 2. Introduction

ExamGuard is a web-based online examination monitoring and integrity analytics platform designed to improve the reliability and transparency of online examinations.

The system combines web-based examination functionality with automated monitoring techniques. It observes examination-related events such as face presence, multiple faces, tab switching, browser focus loss, and audio activity. These events are recorded and assigned different violation weights to calculate an overall examination integrity score.

The platform provides separate interfaces for students and administrators. Students can access and complete examinations, while administrators can monitor examination activity and analyze integrity-related information.

---

## 3. Problem Statement

Online examinations provide flexibility and accessibility, but maintaining examination integrity is challenging when students and invigilators are not physically present in the same location.

Manual monitoring of every student through video calls is difficult to scale and may not provide structured information about suspicious events.

ExamGuard addresses this problem by providing automated monitoring and analytics that can identify predefined examination events and convert them into measurable integrity information.

---

## 4. Objectives

The main objectives of ExamGuard are:

- To provide a web-based online examination environment.
- To monitor student activity during examinations.
- To detect the presence and absence of a student's face.
- To identify situations involving multiple faces.
- To detect browser tab switching.
- To detect loss of browser focus during an examination.
- To monitor unusual audio activity.
- To record examination violations.
- To calculate an integrity score using predefined violation weights.
- To provide administrators with examination and integrity analytics.
- To generate a structured examination integrity report.

---

## 5. Proposed System

ExamGuard provides an integrated examination and monitoring environment.

During an examination, the system collects monitoring events and evaluates them using predefined rules. Each detected event contributes a specific number of points to the violation score.

The system can then classify the examination integrity level based on the calculated score and the configured thresholds.

Administrators can use the administrative interface to review examination activity and integrity information.

---

## 6. Major Features

### 6.1 Student Authentication

Students can access the examination through the student interface.

### 6.2 Online Examination

The system provides an interface through which students can answer examination questions and submit their responses.

### 6.3 Face Monitoring

OpenCV-based computer vision is used to monitor face presence during the examination.

### 6.4 Face Absence Detection

The system records events when the expected face is not detected for the configured monitoring period.

### 6.5 Multiple Face Detection

The system detects situations where more than one face is present in the camera frame.

### 6.6 Browser Tab Monitoring

The system records tab-switching events that occur during the examination.

### 6.7 Browser Focus Monitoring

The system records situations where the examination browser window loses focus.

### 6.8 Audio Monitoring

The system monitors audio activity and records configured audio-spike events.

### 6.9 Integrity Scoring

Detected events are converted into weighted violation points.

### 6.10 Admin Dashboard

Administrators can review examination activity, violations, results, and integrity information.

### 6.11 Automated Report Generation

The project includes LangChain-based processing for generating a narrative examination integrity report from collected information.

---

## 7. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Web Framework | Flask |
| Computer Vision | OpenCV |
| Database Layer | SQLAlchemy |
| Database | SQLite / configured project database |
| Frontend | HTML, CSS, JavaScript |
| AI/NLP Processing | LangChain |
| Development Environment | VS Code |
| Version Control | Git and GitHub |

---

## 8. Monitoring and Violation Weights

ExamGuard uses predefined weights for different monitoring events.

| Monitoring Event | Weight |
|---|---:|
| Tab Switch | 8 |
| Focus Loss | 5 |
| Face Absent | 10 per configured event/minute |
| Multiple Face | 15 |
| Audio Spike | 6 |
| Face Mismatch | 12 |

These values are used by the integrity calculation mechanism to represent the relative contribution of different detected events.

---

## 9. Monitoring Thresholds

The project uses configured thresholds for determining when monitoring events should contribute to the examination integrity analysis.

| Event | Configured Threshold |
|---|---:|
| Tab Switch | 3 |
| Focus Loss | 5 |
| Face Absence | 60 seconds |
| Multiple Face | 1 |
| Audio Spike | 4 |
| Maximum Violations | 5 |
| Maximum Face Absence Events | 5 |
| Maximum Tab Switches | 5 |

These values are configuration parameters and can be adjusted according to examination requirements.

---

## 10. Integrity Classification

ExamGuard uses the accumulated monitoring information to determine an examination integrity level.

The classification is based on the configured scoring and threshold mechanism rather than relying on a single monitoring event.

The system is designed to provide administrators with a structured indication of examination integrity and the events contributing to it.

---

## 11. System Modules

### Student Module

Responsible for:

- Student authentication.
- Examination access.
- Question interaction.
- Answer submission.
- Examination monitoring.

### Monitoring Module

Responsible for:

- Face detection.
- Face absence detection.
- Multiple-face detection.
- Browser tab monitoring.
- Focus monitoring.
- Audio monitoring.
- Violation recording.

### Integrity Analysis Module

Responsible for:

- Applying violation weights.
- Maintaining violation counts.
- Calculating integrity-related information.
- Classifying examination integrity.

### Admin Module

Responsible for:

- Viewing examination information.
- Reviewing violations.
- Reviewing integrity information.
- Accessing analytics.
- Reviewing generated reports.

### Database Module

Responsible for:

- User information.
- Examination information.
- Monitoring information.
- Violation information.
- Results and related records.

### Report Generation Module

Responsible for processing collected examination information and generating a structured narrative report.

---

## 12. Examination Workflow

The general workflow is:

1. Student accesses the student portal.
2. Student authenticates into the system.
3. Student starts the examination.
4. Examination monitoring begins.
5. Webcam-based face monitoring is performed.
6. Browser activity is monitored.
7. Audio activity is monitored according to the configured mechanism.
8. Detected events are recorded.
9. Violation weights are applied.
10. Examination integrity information is calculated.
11. Student submits the examination.
12. Examination information becomes available for administrative review.
13. Administrator reviews results and integrity analytics.
14. A structured report can be generated.

---

## 13. Database

The application uses SQLAlchemy to provide database interaction.

The database layer is responsible for maintaining application information such as:

- User accounts.
- User roles.
- Examination information.
- Student information.
- Monitoring events.
- Violation records.
- Examination results.

---

## 14. Security and Access Control

ExamGuard separates student and administrator functionality.

The system uses role-based access concepts so that students and administrators access the functionality intended for their respective roles.

Authentication information is handled through the application's database and authentication mechanisms.

Sensitive configuration values should be maintained outside the public repository through environment variables or other secure configuration mechanisms.

---

## 15. Advantages

- Automated examination monitoring.
- Structured recording of monitoring events.
- Multiple monitoring signals.
- Weighted integrity analysis.
- Separate student and administrator interfaces.
- Centralized examination information.
- Reduced dependence on continuous manual observation.
- Extensible architecture for future monitoring features.

---

## 16. Limitations

- Computer vision performance can be affected by lighting and camera quality.
- Face detection may be affected by camera positioning.
- Browser monitoring depends on browser-side events.
- Audio monitoring can be affected by environmental noise.
- Automated monitoring events should be interpreted together with examination context.
- Hardware availability is required for camera and audio-based monitoring.

---

## 17. Applications

ExamGuard can be used as a prototype or foundation for:

- College online examinations.
- University assessments.
- Training assessments.
- Certification examinations.
- Remote evaluation systems.
- Controlled online testing environments.

---

## 18. Future Enhancements

Possible future improvements include:

- More robust face recognition.
- Improved anti-spoofing mechanisms.
- Advanced behavioral analysis.
- Better cross-browser compatibility.
- Cloud deployment.
- Scalable multi-student monitoring.
- Improved analytics dashboards.
- More configurable integrity policies.
- Improved accessibility.
- More extensive automated testing.

---

## 19. Conclusion

ExamGuard combines online examination functionality with automated monitoring and integrity analytics.

By integrating computer vision, browser activity monitoring, audio monitoring, weighted violation analysis, database management, and administrative analytics, the project provides a structured approach to online examination monitoring.

The modular design also allows additional monitoring and analytics capabilities to be incorporated in future versions.