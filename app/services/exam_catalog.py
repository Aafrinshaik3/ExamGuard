"""
Domain-specific assessment catalog and curated question bank.
Covers 5 core engineering & technology domains:
1. CSE (Computer Science & Engineering)
2. ECE (Electronics & Communication Engineering)
3. AI & Data Science (Artificial Intelligence & Data Science)
4. EEE (Electrical & Electronics Engineering)
5. Mechanical Engineering (MECH)

Each domain contains 5 standardized assessments, each with 5 multiple-choice questions.
"""

from app import db
from app.models.models import AvailableExam

DOMAIN_CATALOG = {
    "CSE": {
        "domain_name": "Computer Science & Engineering",
        "domain_icon": "💻",
        "exams": [
            {
                "title": "CSE-101: Data Structures & Algorithms",
                "description": "Arrays, linked lists, stacks, queues, trees, graphs, and algorithmic complexity.",
                "duration_minutes": 45,
                "total_questions": 5,
                "questions": [
                    {
                        "id": 1,
                        "text": "Which data structure operates strictly on a LIFO (Last In, First Out) principle?",
                        "options": {"a": "Queue", "b": "Stack", "c": "Binary Tree", "d": "Hash Map"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "What is the worst-case time complexity of QuickSort algorithm?",
                        "options": {"a": "O(n log n)", "b": "O(n²)", "c": "O(log n)", "d": "O(n)"},
                        "answer": "b",
                    },
                    {
                        "id": 3,
                        "text": "Which graph traversal algorithm uses a First-In-First-Out (FIFO) Queue?",
                        "options": {"a": "Breadth-First Search (BFS)", "b": "Depth-First Search (DFS)", "c": "Topological Sort", "d": "Prim's Algorithm"},
                        "answer": "a",
                    },
                    {
                        "id": 4,
                        "text": "In an AVL tree, what is the maximum permissible balance factor for any node?",
                        "options": {"a": "0", "b": "1 (values -1, 0, or +1)", "c": "2", "d": "Any positive integer"},
                        "answer": "b",
                    },
                    {
                        "id": 5,
                        "text": "What is the time complexity to insert a new node at the head of a singly linked list?",
                        "options": {"a": "O(1)", "b": "O(n)", "c": "O(log n)", "d": "O(n²)"},
                        "answer": "a",
                    },
                ],
            },
            {
                "title": "CSE-102: Operating Systems & Architecture",
                "description": "Processes, threads, CPU scheduling, synchronization, deadlocks, and virtual memory.",
                "duration_minutes": 45,
                "total_questions": 5,
                "questions": [
                    {
                        "id": 1,
                        "text": "Which CPU scheduling algorithm is non-preemptive and prone to the convoy effect?",
                        "options": {"a": "Round Robin", "b": "First-Come, First-Served (FCFS)", "c": "Multi-Level Feedback Queue", "d": "Shortest Remaining Time First"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "Which of the following is NOT one of the four Coffman conditions required for a deadlock?",
                        "options": {"a": "Mutual Exclusion", "b": "Hold and Wait", "c": "Preemption allowed", "d": "Circular Wait"},
                        "answer": "c",
                    },
                    {
                        "id": 3,
                        "text": "What is the phenomenon where excessive page swapping degrades system performance to near zero?",
                        "options": {"a": "Thrashing", "b": "External Fragmentation", "c": "Segmentation Fault", "d": "Belady's Anomaly"},
                        "answer": "a",
                    },
                    {
                        "id": 4,
                        "text": "Which POSIX system call creates a new child process duplicating the calling process?",
                        "options": {"a": "exec()", "b": "fork()", "c": "spawn()", "d": "clone_thread()"},
                        "answer": "b",
                    },
                    {
                        "id": 5,
                        "text": "What is the primary role of the Translation Lookaside Buffer (TLB)?",
                        "options": {"a": "Cache recent virtual-to-physical address translations", "b": "Store process control blocks", "c": "Manage disk I/O buffers", "d": "Coordinate interrupt vectors"},
                        "answer": "a",
                    },
                ],
            },
            {
                "title": "CSE-103: Database Management Systems (DBMS)",
                "description": "Relational algebra, SQL, normalization (1NF-BCNF), ACID properties, and indexing.",
                "duration_minutes": 45,
                "total_questions": 5,
                "questions": [
                    {
                        "id": 1,
                        "text": "Which normal form specifically resolves and eliminates transitive functional dependencies?",
                        "options": {"a": "1NF", "b": "2NF", "c": "3NF", "d": "BCNF"},
                        "answer": "c",
                    },
                    {
                        "id": 2,
                        "text": "In ACID transaction management, what does the 'I' represent?",
                        "options": {"a": "Idempotency", "b": "Isolation", "c": "Integrity", "d": "Indexing"},
                        "answer": "b",
                    },
                    {
                        "id": 3,
                        "text": "Which SQL statement deletes all rows from a table without logging individual row deletions?",
                        "options": {"a": "DELETE * FROM table", "b": "TRUNCATE TABLE", "c": "DROP TABLE", "d": "ALTER TABLE REMOVE"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "In a relational database, how many clustered indexes can exist on a single table?",
                        "options": {"a": "Exactly 1", "b": "Up to 16", "c": "One for each column", "d": "Unlimited"},
                        "answer": "a",
                    },
                    {
                        "id": 5,
                        "text": "Which isolation level prevents Dirty Reads but allows Non-Repeatable Reads?",
                        "options": {"a": "Read Uncommitted", "b": "Read Committed", "c": "Repeatable Read", "d": "Serializable"},
                        "answer": "b",
                    },
                ],
            },
            {
                "title": "CSE-104: Computer Networks & Cloud Systems",
                "description": "OSI & TCP/IP layers, routing, switching, DNS/DHCP, transport protocols, and cloud basics.",
                "duration_minutes": 45,
                "total_questions": 5,
                "questions": [
                    {
                        "id": 1,
                        "text": "At which layer of the OSI 7-layer model do routers primarily operate?",
                        "options": {"a": "Data Link Layer (Layer 2)", "b": "Network Layer (Layer 3)", "c": "Transport Layer (Layer 4)", "d": "Session Layer (Layer 5)"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "What is the exact bit length of an IPv6 network address?",
                        "options": {"a": "32 bits", "b": "64 bits", "c": "128 bits", "d": "256 bits"},
                        "answer": "c",
                    },
                    {
                        "id": 3,
                        "text": "During the TCP 3-way handshake, what packet flag(s) does the server send back in response to SYN?",
                        "options": {"a": "SYN", "b": "SYN-ACK", "c": "ACK", "d": "FIN-ACK"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "Which protocol automatically assigns dynamic IP addresses, default gateways, and DNS to network hosts?",
                        "options": {"a": "ARP", "b": "DHCP", "c": "BGP", "d": "ICMP"},
                        "answer": "b",
                    },
                    {
                        "id": 5,
                        "text": "Which cloud service model provides virtual machines, networking, and raw block storage?",
                        "options": {"a": "SaaS", "b": "PaaS", "c": "IaaS", "d": "FaaS"},
                        "answer": "c",
                    },
                ],
            },
            {
                "title": "CSE-105: Object-Oriented Programming (Java & C++)",
                "description": "Inheritance, polymorphism, encapsulation, abstraction, templates, and memory management.",
                "duration_minutes": 45,
                "total_questions": 5,
                "questions": [
                    {
                        "id": 1,
                        "text": "Which OOP principle allows the same method call to execute different behaviors based on the object type at runtime?",
                        "options": {"a": "Encapsulation", "b": "Dynamic Polymorphism (Overriding)", "c": "Data Hiding", "d": "Multiple Inheritance"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "In Java, which keyword is applied to a class to prevent other classes from inheriting from it?",
                        "options": {"a": "static", "b": "final", "c": "abstract", "d": "const"},
                        "answer": "b",
                    },
                    {
                        "id": 3,
                        "text": "In C++, what is the default member access specifier for a `class` if none is declared?",
                        "options": {"a": "public", "b": "private", "c": "protected", "d": "friend"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "Which Java Collection Framework interface represents an unordered collection that permits no duplicate elements?",
                        "options": {"a": "List", "b": "Set", "c": "Queue", "d": "Vector"},
                        "answer": "b",
                    },
                    {
                        "id": 5,
                        "text": "What type of pointer in C++ automatically releases its owned dynamic heap memory when it leaves scope?",
                        "options": {"a": "Raw pointer (*)", "b": "std::unique_ptr", "c": "void*", "d": "Volatile pointer"},
                        "answer": "b",
                    },
                ],
            },
        ],
    },

    "ECE": {
        "domain_name": "Electronics & Communication Engineering",
        "domain_icon": "⚡",
        "exams": [
            {
                "title": "ECE-101: Digital Electronics & Logic Design",
                "description": "Boolean algebra, logic gates, combinational circuits, flip-flops, and finite state machines.",
                "duration_minutes": 45,
                "total_questions": 5,
                "questions": [
                    {
                        "id": 1,
                        "text": "How many select input lines are required for a 32-to-1 Multiplexer (MUX)?",
                        "options": {"a": "4", "b": "5", "c": "8", "d": "16"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "Which of the following gate pairs are universal gates capable of implementing any Boolean function?",
                        "options": {"a": "AND and OR", "b": "NAND and NOR", "c": "XOR and XNOR", "d": "NOT and AND"},
                        "answer": "b",
                    },
                    {
                        "id": 3,
                        "text": "What is the 2's complement representation of the binary byte 00001010 (+10 in decimal)?",
                        "options": {"a": "11110101", "b": "11110110", "c": "11110111", "d": "10001010"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "Which flip-flop resolves the invalid indeterminate state of an SR latch when both inputs are 1?",
                        "options": {"a": "D Flip-Flop", "b": "JK Flip-Flop", "c": "T Flip-Flop", "d": "Transparent Latch"},
                        "answer": "b",
                    },
                    {
                        "id": 5,
                        "text": "According to De Morgan's Law, the complement of a product (A · B)' is equivalent to:",
                        "options": {"a": "A' · B'", "b": "A' + B'", "c": "(A + B)'", "d": "A + B"},
                        "answer": "b",
                    },
                ],
            },
            {
                "title": "ECE-102: Signals, Systems & DSP",
                "description": "Fourier analysis, sampling theorem, LTI systems, Z-transform, and digital filter structures.",
                "duration_minutes": 45,
                "total_questions": 5,
                "questions": [
                    {
                        "id": 1,
                        "text": "According to the Nyquist-Shannon sampling theorem, to prevent aliasing, sampling rate Fs must satisfy:",
                        "options": {"a": "Fs ≤ Fm", "b": "Fs ≥ 2 · Fm", "c": "Fs = Fm / 2", "d": "Fs ≥ 4 · Fm"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "What is the continuous-time Fourier Transform of an ideal unit impulse function δ(t)?",
                        "options": {"a": "0", "b": "1", "c": "e^(-jω)", "d": "2πδ(ω)"},
                        "answer": "b",
                    },
                    {
                        "id": 3,
                        "text": "For a discrete-time causal LTI system to be bounded-input bounded-output (BIBO) stable, all poles must be located:",
                        "options": {"a": "Outside the unit circle in the Z-plane", "b": "Strictly inside the unit circle (|z| < 1)", "c": "On the imaginary axis", "d": "In the left-half of the S-plane only"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "What computational efficiency does the Fast Fourier Transform (FFT) achieve over direct DFT for N points?",
                        "options": {"a": "Reduces operations from O(N²) to O(N log₂ N)", "b": "Reduces operations from O(N³) to O(N²)", "c": "Achieves O(1) constant time", "d": "Eliminates complex multiplication completely"},
                        "answer": "a",
                    },
                    {
                        "id": 5,
                        "text": "Which filter design class is guaranteed to exhibit strictly linear phase response?",
                        "options": {"a": "IIR Butterworth filter", "b": "IIR Chebyshev filter", "c": "Symmetric FIR filter", "d": "Elliptic Cauer filter"},
                        "answer": "c",
                    },
                ],
            },
            {
                "title": "ECE-103: Microprocessors & Embedded Systems",
                "description": "8085 architecture, 8051 microcontrollers, ARM Cortex registers, interrupts, and interfacing.",
                "duration_minutes": 45,
                "total_questions": 5,
                "questions": [
                    {
                        "id": 1,
                        "text": "What is the bit-width of the program counter (PC) in the classic 8085 microprocessor?",
                        "options": {"a": "8 bits", "b": "16 bits", "c": "32 bits", "d": "64 bits"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "Which 8085 hardware interrupt is non-maskable and possesses the highest priority?",
                        "options": {"a": "RST 7.5", "b": "INTR", "c": "TRAP (RST 4.5)", "d": "RST 5.5"},
                        "answer": "c",
                    },
                    {
                        "id": 3,
                        "text": "How many bidirectional 8-bit parallel I/O ports are provided on a standard 8051 microcontroller?",
                        "options": {"a": "2 ports (16 lines)", "b": "4 ports (32 lines)", "c": "6 ports (48 lines)", "d": "8 ports"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "In ARM Cortex-M processors, which register serves as the Link Register (LR) storing return addresses?",
                        "options": {"a": "R12", "b": "R13 (SP)", "c": "R14 (LR)", "d": "R15 (PC)"},
                        "answer": "c",
                    },
                    {
                        "id": 5,
                        "text": "Which serial communication bus uses two bidirectional lines: Serial Clock (SCL) and Serial Data (SDA)?",
                        "options": {"a": "SPI", "b": "I2C", "c": "UART", "d": "CAN bus"},
                        "answer": "b",
                    },
                ],
            },
            {
                "title": "ECE-104: Analog & Digital Communications",
                "description": "Modulation (AM, FM, PM), digital keying (ASK, FSK, PSK, QAM), noise figures, and multiplexing.",
                "duration_minutes": 45,
                "total_questions": 5,
                "questions": [
                    {
                        "id": 1,
                        "text": "In Amplitude Modulation (AM), what undesirable effect occurs if modulation index m > 1.0?",
                        "options": {"a": "Under-modulation", "b": "Over-modulation causing envelope distortion and carrier clipping", "c": "Bandwidth reduction", "d": "Power reduction in sidebands"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "According to Carson's Rule, the approximate transmission bandwidth required for an FM wave is:",
                        "options": {"a": "2 · Δf", "b": "2 · (Δf + fm)", "c": "Δf / fm", "d": "4 · fm"},
                        "answer": "b",
                    },
                    {
                        "id": 3,
                        "text": "Which digital modulation scheme conveys information by altering the phase of the carrier signal among discrete states?",
                        "options": {"a": "ASK", "b": "PSK (Phase Shift Keying)", "c": "FSK", "d": "PWM"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "What is the primary function of a Matched Filter at the receiver stage of a digital transmission link?",
                        "options": {"a": "Equalize carrier phase drift", "b": "Maximize output Signal-to-Noise Ratio (SNR) at sampling instant", "c": "Perform analog-to-digital conversion", "d": "Eliminate inter-carrier interference in OFDM"},
                        "answer": "b",
                    },
                    {
                        "id": 5,
                        "text": "In Pulse Code Modulation (PCM), what is the key process that converts continuous sample amplitudes into discrete levels?",
                        "options": {"a": "Sampling", "b": "Quantization", "c": "Encoding", "d": "Multiplexing"},
                        "answer": "b",
                    },
                ],
            },
            {
                "title": "ECE-105: VLSI Design & Semiconductor Devices",
                "description": "MOSFET physics, CMOS inverter characteristics, layout rules, propagation delay, and ASIC flows.",
                "duration_minutes": 45,
                "total_questions": 5,
                "questions": [
                    {
                        "id": 1,
                        "text": "Why do NMOS transistors exhibit higher switching speed than PMOS transistors of identical dimensions?",
                        "options": {"a": "Electrons have higher mobility than holes in silicon", "b": "Holes have lower mass than electrons", "c": "PMOS requires higher threshold voltage", "d": "NMOS oxide is thinner"},
                        "answer": "a",
                    },
                    {
                        "id": 2,
                        "text": "In a static CMOS inverter under steady-state quiescent conditions, the DC power dissipation is:",
                        "options": {"a": "Extremely high due to continuous conduction", "b": "Virtually zero (dominated solely by subthreshold leakage)", "c": "Linearly proportional to clock frequency", "d": "Equal to C · V² · f"},
                        "answer": "b",
                    },
                    {
                        "id": 3,
                        "text": "What is the short-channel effect where the drain depletion region merges with the source depletion region?",
                        "options": {"a": "Velocity saturation", "b": "Punch-through", "c": "Hot-carrier injection", "d": "Drain-induced barrier lowering (DIBL)"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "What destructive phenomenon in bulk CMOS occurs due to parasitic bipolar npn and pnp transistors forming an SCR structure?",
                        "options": {"a": "Electrostatic discharge (ESD)", "b": "Latch-up", "c": "Electromigration", "d": "Dielectric breakdown"},
                        "answer": "b",
                    },
                    {
                        "id": 5,
                        "text": "In modern FPGA and ASIC design, which hardware description language (HDL) standard is most commonly used alongside Verilog?",
                        "options": {"a": "VHDL", "b": "Fortran", "c": "MATLAB", "d": "Assembly"},
                        "answer": "a",
                    },
                ],
            },
        ],
    },

    "AI & Data Science": {
        "domain_name": "Artificial Intelligence & Data Science",
        "domain_icon": "🤖",
        "exams": [
            {
                "title": "AIDS-101: Machine Learning & Predictive Modeling",
                "description": "Supervised & unsupervised learning, bias-variance tradeoff, regularization, and evaluation metrics.",
                "duration_minutes": 45,
                "total_questions": 5,
                "questions": [
                    {
                        "id": 1,
                        "text": "A model that performs exceptionally on training data but poorly on unseen test data is experiencing:",
                        "options": {"a": "High bias (Underfitting)", "b": "High variance (Overfitting)", "c": "Optimal convergence", "d": "Data leakage"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "Which regularization technique adds the absolute sum of coefficients (L1 penalty) encouraging sparse weights?",
                        "options": {"a": "Ridge Regression", "b": "Lasso Regression", "c": "Elastic Net with L1=0", "d": "Dropout"},
                        "answer": "b",
                    },
                    {
                        "id": 3,
                        "text": "In a classification model evaluating rare disease detection, which metric is most crucial to minimize False Negatives?",
                        "options": {"a": "Precision", "b": "Recall (Sensitivity)", "c": "Specificity", "d": "Accuracy"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "Which ensemble algorithm constructs sequential trees by assigning higher sample weights to misclassified instances?",
                        "options": {"a": "Random Forest", "b": "AdaBoost / Gradient Boosting", "c": "Bagging Classifier", "d": "Extra Trees"},
                        "answer": "b",
                    },
                    {
                        "id": 5,
                        "text": "What does the Area Under the ROC Curve (AUC-ROC) score measure for a binary classifier?",
                        "options": {"a": "Mean squared error of probabilities", "b": "Ability to distinguish positive instances from negative across all decision thresholds", "c": "Training time complexity", "d": "Data clustering density"},
                        "answer": "b",
                    },
                ],
            },
            {
                "title": "AIDS-102: Deep Learning & Neural Networks",
                "description": "Backpropagation, activation functions, CNNs, RNNs, vanishing gradients, and optimization algorithms.",
                "duration_minutes": 45,
                "total_questions": 5,
                "questions": [
                    {
                        "id": 1,
                        "text": "Which activation function computes f(x) = max(0, x) and helps mitigate vanishing gradients in hidden layers?",
                        "options": {"a": "Sigmoid", "b": "ReLU (Rectified Linear Unit)", "c": "Tanh", "d": "Softmax"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "In Convolutional Neural Networks (CNNs), what operation reduces spatial dimensions while retaining dominant features?",
                        "options": {"a": "Batch Normalization", "b": "Max Pooling", "c": "Zero Padding", "d": "Residual Connection"},
                        "answer": "b",
                    },
                    {
                        "id": 3,
                        "text": "Which optimizer combines the benefits of AdaGrad (adaptive learning rates) and RMSprop (moving average squared gradients)?",
                        "options": {"a": "SGD with Momentum", "b": "Adam", "c": "Nesterov Accelerated Gradient", "d": "L-BFGS"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "What regularization method randomly deactivates a fraction of neurons and their connections during training passes?",
                        "options": {"a": "Weight decay", "b": "Dropout", "c": "Data Augmentation", "d": "Gradient Clipping"},
                        "answer": "b",
                    },
                    {
                        "id": 5,
                        "text": "What architectural innovation in ResNet allows training extremely deep networks (e.g. 152 layers) without gradient degradation?",
                        "options": {"a": "Skip / Residual connections", "b": "Recurrent loops", "c": "Bilinear interpolation", "d": "Self-attention heads"},
                        "answer": "a",
                    },
                ],
            },
            {
                "title": "AIDS-103: Natural Language Processing & Transformers",
                "description": "Tokenization, word embeddings, self-attention, Transformer architecture, BERT, and GPT fundamentals.",
                "duration_minutes": 45,
                "total_questions": 5,
                "questions": [
                    {
                        "id": 1,
                        "text": "In the standard Transformer architecture, which mechanism allows tokens to weigh relationships across the entire sequence simultaneously?",
                        "options": {"a": "Convolutional stride", "b": "Multi-Head Self-Attention", "c": "Bidirectional LSTM gates", "d": "Markov Chain transition"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "What mathematical vector representation technique generates dense semantic word vectors using Continuous Bag-of-Words (CBOW) or Skip-gram?",
                        "options": {"a": "TF-IDF", "b": "Word2Vec", "c": "One-Hot Encoding", "d": "Bag of Words (BoW)"},
                        "answer": "b",
                    },
                    {
                        "id": 3,
                        "text": "Which foundational Transformer model is designed as a bidirectional encoder trained on Masked Language Modeling (MLM)?",
                        "options": {"a": "GPT-3", "b": "BERT", "c": "LLaMA", "d": "T5 Decoder"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "Why are Positional Encodings added to input embeddings in Transformer models?",
                        "options": {"a": "To normalize token amplitudes", "b": "To supply sequential order information since attention operations are permutation-invariant", "c": "To prevent overfitting on vocabulary", "d": "To compress vocabulary dimension"},
                        "answer": "b",
                    },
                    {
                        "id": 5,
                        "text": "Which temperature parameter setting in autoregressive language models generates the most deterministic and focused output?",
                        "options": {"a": "temperature = 0.0 (or very low)", "b": "temperature = 1.0", "c": "temperature = 2.5", "d": "temperature = 10.0"},
                        "answer": "a",
                    },
                ],
            },
            {
                "title": "AIDS-104: Computer Vision & Image Processing",
                "description": "Image filtering, edge detection, object detection (YOLO), segmentation, and OpenCV techniques.",
                "duration_minutes": 45,
                "total_questions": 5,
                "questions": [
                    {
                        "id": 1,
                        "text": "Which edge detection algorithm uses Gaussian smoothing, gradient magnitude calculation, non-maximum suppression, and hysteresis thresholding?",
                        "options": {"a": "Sobel Operator", "b": "Canny Edge Detector", "c": "Prewitt Filter", "d": "Laplacian of Gaussian"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "In object detection, what metric measures the overlap between a predicted bounding box and the ground truth box?",
                        "options": {"a": "Cosine Distance", "b": "Intersection over Union (IoU)", "c": "Mean Absolute Error", "d": "Structural Similarity Index (SSIM)"},
                        "answer": "b",
                    },
                    {
                        "id": 3,
                        "text": "What post-processing step in YOLO filters out redundant duplicate bounding boxes corresponding to the same detected object?",
                        "options": {"a": "Anchor clustering", "b": "Non-Maximum Suppression (NMS)", "c": "Spatial Pyramid Pooling", "d": "Feature Pyramid Decoupling"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "In digital image processing, what does applying a 2D Gaussian blur kernel to an image achieve?",
                        "options": {"a": "Edge sharpening", "b": "High-frequency noise attenuation (smoothing)", "c": "Color inversion", "d": "Contrast stretching"},
                        "answer": "b",
                    },
                    {
                        "id": 5,
                        "text": "Which task classifies every individual pixel in an input image into a corresponding semantic category?",
                        "options": {"a": "Image Classification", "b": "Semantic Segmentation", "c": "Object Localization", "d": "Keypoint Detection"},
                        "answer": "b",
                    },
                ],
            },
            {
                "title": "AIDS-105: Data Analytics & Feature Engineering",
                "description": "Data preprocessing, PCA, feature scaling, hypothesis testing, and statistical inferences.",
                "duration_minutes": 45,
                "total_questions": 5,
                "questions": [
                    {
                        "id": 1,
                        "text": "Which dimensionality reduction method identifies orthogonal axes maximizing variance in high-dimensional feature spaces?",
                        "options": {"a": "K-Means", "b": "Principal Component Analysis (PCA)", "c": "Linear Discriminant Analysis", "d": "t-SNE for compression"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "When scaling features with StandardScaler (Z-score normalization), what are the resulting mean and variance?",
                        "options": {"a": "Mean = 0, Standard Deviation = 1", "b": "Min = 0, Max = 1", "c": "Mean = 1, Variance = 0", "d": "Range [-1, +1]"},
                        "answer": "a",
                    },
                    {
                        "id": 3,
                        "text": "In hypothesis testing, rejecting a true null hypothesis (false alarm) is known as:",
                        "options": {"a": "Type I Error (α)", "b": "Type II Error (β)", "c": "Sampling Bias", "d": "Standard Error"},
                        "answer": "a",
                    },
                    {
                        "id": 4,
                        "text": "Which statistical correlation coefficient quantifies linear relationship strength between two continuous variables on a scale [-1, +1]?",
                        "options": {"a": "Spearman Rank Correlation", "b": "Pearson Correlation Coefficient (r)", "c": "Kendall Tau", "d": "Chi-Square statistic"},
                        "answer": "b",
                    },
                    {
                        "id": 5,
                        "text": "What encoding method transforms a categorical feature with N nominal categories into N binary indicator columns?",
                        "options": {"a": "Ordinal Encoding", "b": "One-Hot Encoding", "c": "Frequency Encoding", "d": "Target Encoding"},
                        "answer": "b",
                    },
                ],
            },
        ],
    },

    "EEE": {
        "domain_name": "Electrical & Electronics Engineering",
        "domain_icon": "🔋",
        "exams": [
            {
                "title": "EEE-101: Circuit Theory & Network Analysis",
                "description": "Kirchhoff's laws, Thevenin & Norton theorems, transient response, and RLC resonance.",
                "duration_minutes": 45,
                "total_questions": 5,
                "questions": [
                    {
                        "id": 1,
                        "text": "According to Kirchhoff's Current Law (KCL), what is the algebraic sum of currents entering any electrical node?",
                        "options": {"a": "Equal to total voltage", "b": "Exactly zero", "c": "Equal to circuit impedance", "d": "Infinite"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "According to Thevenin's Theorem, any linear two-terminal bilateral network can be replaced by:",
                        "options": {"a": "A single current source in parallel with resistance", "b": "A single independent voltage source (Vth) in series with equivalent resistance (Rth)", "c": "An ideal capacitor and inductor", "d": "A pure conductance bridge"},
                        "answer": "b",
                    },
                    {
                        "id": 3,
                        "text": "In a series RLC circuit at resonant frequency fr, what is the net circuit impedance?",
                        "options": {"a": "Purely resistive (Z = R) and at minimum", "b": "Purely inductive (Z = jωL)", "c": "Purely capacitive (Z = 1/jωC)", "d": "Infinite"},
                        "answer": "a",
                    },
                    {
                        "id": 4,
                        "text": "For maximum power transfer from a DC voltage source to a variable load resistor RL, RL must equal:",
                        "options": {"a": "0 Ohms", "b": "The internal source resistance Rth", "c": "Twice the source resistance", "d": "Infinity"},
                        "answer": "b",
                    },
                    {
                        "id": 5,
                        "text": "What is the steady-state DC impedance of an ideal inductor (L)?",
                        "options": {"a": "Infinite (Open circuit)", "b": "Zero (Short circuit)", "c": "Dependent on permeability", "d": "Equal to capacitive reactance"},
                        "answer": "b",
                    },
                ],
            },
            {
                "title": "EEE-102: Control Systems Engineering",
                "description": "Transfer functions, Routh-Hurwitz stability, Bode plots, root locus, and PID controllers.",
                "duration_minutes": 45,
                "total_questions": 5,
                "questions": [
                    {
                        "id": 1,
                        "text": "A linear time-invariant system is strictly stable if all closed-loop poles lie in:",
                        "options": {"a": "The right half of the s-plane", "b": "The open left-half of the s-plane (Re(s) < 0)", "c": "On the jω imaginary axis", "d": "At the origin"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "In a Bode diagram, what is the Gain Margin defined as at the phase crossover frequency (where phase = -180°)?",
                        "options": {"a": "The reciprocal of the open-loop gain magnitude (1/|G(jω)|)", "b": "The phase shift at 0 dB gain", "c": "The system resonant peak", "d": "The damping ratio"},
                        "answer": "a",
                    },
                    {
                        "id": 3,
                        "text": "In a PID controller, which term is primarily responsible for eliminating steady-state error?",
                        "options": {"a": "Proportional (P) term", "b": "Integral (I) term", "c": "Derivative (D) term", "d": "Feedforward gain"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "According to the Routh-Hurwitz criterion, how is the number of unstable right-half plane poles determined?",
                        "options": {"a": "Number of sign changes in the first column of the Routh array", "b": "Number of zeros in the characteristic equation", "c": "The highest power of s", "d": "The determinant of state matrix"},
                        "answer": "a",
                    },
                    {
                        "id": 5,
                        "text": "Adding a pole to an open-loop transfer function typically shifts the root locus toward the right, resulting in:",
                        "options": {"a": "Increased system stability", "b": "Reduced system stability and slower response", "c": "Zero overshoot", "d": "Immediate oscillation"},
                        "answer": "b",
                    },
                ],
            },
            {
                "title": "EEE-103: Electrical Machines & Transformers",
                "description": "Transformers, induction motors, synchronous machines, DC motors, and efficiency calculations.",
                "duration_minutes": 45,
                "total_questions": 5,
                "questions": [
                    {
                        "id": 1,
                        "text": "In an ideal power transformer under no-load conditions, how is the core loss (iron loss) primarily measured?",
                        "options": {"a": "Short-Circuit Test", "b": "Open-Circuit Test", "c": "Sumpner's Back-to-Back Test", "d": "Insulation Resistance Test"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "In a 3-phase induction motor, what is the slip (s) when the rotor rotates at synchronous speed (Ns)?",
                        "options": {"a": "s = 1.0 (100%)", "b": "s = 0.0", "c": "s = -1.0", "d": "s = infinity"},
                        "answer": "b",
                    },
                    {
                        "id": 3,
                        "text": "What type of DC motor provides the highest starting torque and is widely utilized in electric traction systems?",
                        "options": {"a": "DC Shunt Motor", "b": "DC Series Motor", "c": "Cumulative Compound Motor", "d": "Permanent Magnet Brushless Motor"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "What causes the laminated construction of transformer cores and alternator stators?",
                        "options": {"a": "Reduce hysteresis loss", "b": "Minimize eddy current losses", "c": "Prevent mechanical vibration", "d": "Increase magnetic reluctance"},
                        "answer": "b",
                    },
                    {
                        "id": 5,
                        "text": "In a synchronous alternator, what is the effect of an over-excited rotor field on the power factor?",
                        "options": {"a": "Causes lagging power factor", "b": "Causes leading power factor (supplies reactive power)", "c": "Operates strictly at unity", "d": "Zero power factor lagging"},
                        "answer": "b",
                    },
                ],
            },
            {
                "title": "EEE-104: Power Systems Analysis & Protection",
                "description": "Transmission line modeling, fault analysis, protective relays, circuit breakers, and power flow.",
                "duration_minutes": 45,
                "total_questions": 5,
                "questions": [
                    {
                        "id": 1,
                        "text": "Which iterative numerical method converges quadratically and is widely used for power flow (load flow) analysis?",
                        "options": {"a": "Gauss-Seidel Method", "b": "Newton-Raphson Method", "c": "Euler-Cauchy Method", "d": "Fast Decoupled only for DC"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "What phenomenon causes AC current density to concentrate near the outer surface of a conductor, increasing resistance?",
                        "options": {"a": "Proximity effect", "b": "Skin effect", "c": "Ferranti effect", "d": "Corona discharge"},
                        "answer": "b",
                    },
                    {
                        "id": 3,
                        "text": "The Ferranti effect in high-voltage AC transmission lines refers to the situation where:",
                        "options": {"a": "Sending end voltage is higher than receiving end", "b": "Receiving end voltage exceeds sending end voltage under light load or no load", "c": "Power factor approaches zero lagging", "d": "Frequency drops abruptly"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "Which protective relay principle operates based on the vector difference between currents entering and leaving the protected zone?",
                        "options": {"a": "Overcurrent relay", "b": "Differential relay", "c": "Distance relay (Mho)", "d": "Directional relay"},
                        "answer": "b",
                    },
                    {
                        "id": 5,
                        "text": "Which symmetrical components exist during a purely balanced three-phase fault?",
                        "options": {"a": "Positive-sequence components only", "b": "Negative-sequence components only", "c": "Zero-sequence components only", "d": "Both positive and zero sequence"},
                        "answer": "a",
                    },
                ],
            },
            {
                "title": "EEE-105: Power Electronics & Industrial Drives",
                "description": "Thyristors (SCR), DC-DC converters (Buck, Boost), inverters, PWM modulation, and motor drives.",
                "duration_minutes": 45,
                "total_questions": 5,
                "questions": [
                    {
                        "id": 1,
                        "text": "Once a Silicon Controlled Rectifier (SCR) is triggered into conduction, how can it be turned off (commutated)?",
                        "options": {"a": "Applying negative gate pulse", "b": "Reducing the anode current below the holding current (Ih)", "c": "Increasing gate bias voltage", "d": "Disconnecting the gate terminal"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "In a DC-DC Buck converter operating in continuous conduction mode (CCM), the output voltage Vo relates to input Vs by:",
                        "options": {"a": "Vo = Vs · D (where D is duty ratio)", "b": "Vo = Vs / (1 - D)", "c": "Vo = Vs · (1 - D)", "d": "Vo = Vs / D"},
                        "answer": "a",
                    },
                    {
                        "id": 3,
                        "text": "Which power semiconductor switch combines the high input impedance of a MOSFET with the low conduction loss of a BJT?",
                        "options": {"a": "TRIAC", "b": "IGBT (Insulated Gate Bipolar Transistor)", "c": "GTO Thyristor", "d": "Power Diode"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "In Sinusoidal Pulse Width Modulation (SPWM) inverters, what controls the fundamental output AC frequency?",
                        "options": {"a": "The high-frequency triangular carrier wave", "b": "The low-frequency sinusoidal reference modulating wave", "c": "The DC link bus capacitor size", "d": "Dead-time generator"},
                        "answer": "b",
                    },
                    {
                        "id": 5,
                        "text": "What is the standard technique for variable speed AC induction motor drives to keep magnetic flux constant below base speed?",
                        "options": {"a": "V/f (Voltage to Frequency) control constant ratio", "b": "Constant rotor resistance control", "c": "Field weakening control", "d": "Direct line switching"},
                        "answer": "a",
                    },
                ],
            },
        ],
    },

    "Mechanical": {
        "domain_name": "Mechanical Engineering",
        "domain_icon": "⚙️",
        "exams": [
            {
                "title": "MECH-101: Engineering Thermodynamics & Heat Transfer",
                "description": "Thermodynamic laws, cycles (Carnot, Otto, Rankine), conduction, convection, and radiation.",
                "duration_minutes": 45,
                "total_questions": 5,
                "questions": [
                    {
                        "id": 1,
                        "text": "Which theoretical heat engine cycle operates between two temperature limits with the highest possible thermal efficiency?",
                        "options": {"a": "Otto Cycle", "b": "Carnot Cycle", "c": "Rankine Cycle", "d": "Diesel Cycle"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "The Second Law of Thermodynamics dictates that the total entropy of an isolated system over any spontaneous process:",
                        "options": {"a": "Always decreases", "b": "Always increases or remains constant (ΔS ≥ 0)", "c": "Remains strictly zero", "d": "Fluctuates sinusoidally"},
                        "answer": "b",
                    },
                    {
                        "id": 3,
                        "text": "According to Fourier's Law of heat conduction, heat transfer rate Q is directly proportional to:",
                        "options": {"a": "Temperature gradient (dT/dx) and cross-sectional area", "b": "Fourth power of absolute temperature", "c": "Convective film coefficient only", "d": "Emissivity of boundary layer"},
                        "answer": "a",
                    },
                    {
                        "id": 4,
                        "text": "According to the Stefan-Boltzmann Law, total thermal radiation power emitted by a blackbody is proportional to:",
                        "options": {"a": "T", "b": "T²", "c": "T³", "d": "T⁴ (fourth power of absolute temperature)"},
                        "answer": "d",
                    },
                    {
                        "id": 5,
                        "text": "In a steam power plant operating on the Rankine cycle, which component increases feedwater pressure to boiler pressure?",
                        "options": {"a": "Condenser", "b": "Boiler economizer", "c": "Feed pump", "d": "Steam turbine"},
                        "answer": "c",
                    },
                ],
            },
            {
                "title": "MECH-102: Fluid Mechanics & Hydraulic Machinery",
                "description": "Fluid statics, Bernoulli's equation, laminar vs turbulent flow, boundary layers, and hydraulic turbines.",
                "duration_minutes": 45,
                "total_questions": 5,
                "questions": [
                    {
                        "id": 1,
                        "text": "For flow through a circular pipe, the Reynolds number (Re) threshold typically demarcating laminar from turbulent flow is:",
                        "options": {"a": "Re < 500", "b": "Re ≈ 2000 to 2300", "c": "Re > 100,000", "d": "Re = 1.0"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "Bernoulli's equation applies along a streamline for fluid flow that is assumed to be:",
                        "options": {"a": "Steady, incompressible, frictionless (inviscid), and irrotational", "b": "Compressible and turbulent", "c": "Unsteady and viscous", "d": "Non-Newtonian boundary layer"},
                        "answer": "a",
                    },
                    {
                        "id": 3,
                        "text": "Which hydraulic turbine is classified as a tangential-flow high-head impulse turbine?",
                        "options": {"a": "Francis Turbine", "b": "Pelton Wheel Turbine", "c": "Kaplan Turbine", "d": "Propeller Turbine"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "What device measures volumetric flow rate in a pipeline by creating a constriction and measuring differential pressure?",
                        "options": {"a": "Pitot tube", "b": "Venturimeter / Orifice plate", "c": "Bourdon gauge", "d": "Manometer only for density"},
                        "answer": "b",
                    },
                    {
                        "id": 5,
                        "text": "What phenomenon occurs in pumps when local static liquid pressure drops below saturated vapor pressure, collapsing bubbles?",
                        "options": {"a": "Water hammer", "b": "Cavitation", "c": "Surge", "d": "Boundary separation"},
                        "answer": "b",
                    },
                ],
            },
            {
                "title": "MECH-103: Strength of Materials & Solid Mechanics",
                "description": "Stress-strain, Hooke's law, Mohr's circle, bending theory, torsion of shafts, and Euler column buckling.",
                "duration_minutes": 45,
                "total_questions": 5,
                "questions": [
                    {
                        "id": 1,
                        "text": "In the elastic deformation range of an isotropic material, Hooke's law states that stress is directly proportional to:",
                        "options": {"a": "Temperature", "b": "Strain", "c": "Plastic yield modulus", "d": "Poisson's ratio"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "In the standard flexural formula for pure beam bending (M/I = σ/y = E/R), what does 'I' represent?",
                        "options": {"a": "Area moment of inertia of the beam cross-section about neutral axis", "b": "Polar moment of inertia", "c": "Length of the beam span", "d": "Curvature radius"},
                        "answer": "a",
                    },
                    {
                        "id": 3,
                        "text": "What graphical method determines principal stresses, maximum shear stresses, and plane orientations from a 2D stress state?",
                        "options": {"a": "S-N Curve", "b": "Mohr's Circle of Stress", "c": "Goodman Diagram", "d": "Miner's Cumulative Law"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "According to Euler's buckling formula for long slender columns, critical buckling load Pcr is proportional to:",
                        "options": {"a": "Column length L", "b": "1 / L² (inversely proportional to square of effective length)", "c": "Yield strength σy", "d": "Cross-sectional perimeter"},
                        "answer": "b",
                    },
                    {
                        "id": 5,
                        "text": "When a solid circular cylindrical shaft of diameter D is subjected to pure torque T, maximum shear stress occurs at:",
                        "options": {"a": "The shaft center axis", "b": "The outer surface perimeter of the shaft", "c": "At D/4 from the center", "d": "Evenly throughout the volume"},
                        "answer": "b",
                    },
                ],
            },
            {
                "title": "MECH-104: Theory of Machines & Kinematics",
                "description": "Four-bar linkages, Grashof criterion, gears & epicyclic gear trains, cams, and gyroscopic couples.",
                "duration_minutes": 45,
                "total_questions": 5,
                "questions": [
                    {
                        "id": 1,
                        "text": "According to Grashof's law for a 4-bar planar mechanism, continuous relative rotation of at least one link is possible if:",
                        "options": {"a": "s + l ≤ p + q (sum of shortest and longest links ≤ sum of remaining two)", "b": "s + l > p + q", "c": "All links are of equal length", "d": "The shortest link is fixed as the frame"},
                        "answer": "a",
                    },
                    {
                        "id": 2,
                        "text": "To prevent tooth interference and undercutting in standard 20° pressure angle involute spur gears, minimum teeth on pinion is:",
                        "options": {"a": "8", "b": "17 (or 18)", "c": "32", "d": "45"},
                        "answer": "b",
                    },
                    {
                        "id": 3,
                        "text": "In epicyclic (planetary) gear trains, which component typically carries the planet gears rotating around the sun gear?",
                        "options": {"a": "Ring / Annulus gear", "b": "Planet carrier (Arm)", "c": "Counter-shaft", "d": "Differential pinion"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "The gyroscopic couple C acting on a rotating disc of polar moment of inertia I spinning at ω with precession rate ωp is:",
                        "options": {"a": "C = I · ω · ωp", "b": "C = I · ω²", "c": "C = I / (ω · ωp)", "d": "C = 0.5 · I · ωp"},
                        "answer": "a",
                    },
                    {
                        "id": 5,
                        "text": "Which kinematic inversion of a single slider-crank mechanism forms the basis of the Whitworth quick return motion mechanism?",
                        "options": {"a": "Fixing the crank link", "b": "Fixing the connecting rod or slotted lever", "c": "Fixing the cylinder frame", "d": "Fixing the piston slider"},
                        "answer": "b",
                    },
                ],
            },
            {
                "title": "MECH-105: Manufacturing Processes & CAD/CAM",
                "description": "Machining (Taylor's tool life), casting (Chvorinov's rule), welding (TIG/MIG), CNC G-codes, and 3D printing.",
                "duration_minutes": 45,
                "total_questions": 5,
                "questions": [
                    {
                        "id": 1,
                        "text": "According to Taylor's Tool Life Equation (V · T^n = C), increasing cutting speed V results in:",
                        "options": {"a": "Longer tool life T", "b": "Exponentially reduced tool life T", "c": "No change in tool life", "d": "Zero cutting temperature"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "According to Chvorinov's Rule, the solidification time of a metal casting mold is proportional to:",
                        "options": {"a": "Surface Area / Volume", "b": "(Volume / Surface Area)²", "c": "Pouring temperature only", "d": "Mold sand permeability"},
                        "answer": "b",
                    },
                    {
                        "id": 3,
                        "text": "In Gas Tungsten Arc Welding (GTAW / TIG), what type of electrode is utilized during welding operations?",
                        "options": {"a": "Consumable flux-coated steel electrode", "b": "Non-consumable pure or thoriated tungsten electrode", "c": "Copper-coated wire spool", "d": "Graphite rod"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "In standard CNC machine programming (ISO / EIA), which preparatory G-code specifies rapid non-cutting positioning?",
                        "options": {"a": "G00", "b": "G01 (Linear interpolation)", "c": "G02 (Circular CW)", "d": "G03 (Circular CCW)"},
                        "answer": "a",
                    },
                    {
                        "id": 5,
                        "text": "Which additive manufacturing technique deposits thermoplastic filament layer-by-layer through a heated extrusion nozzle?",
                        "options": {"a": "Selective Laser Sintering (SLS)", "b": "Fused Deposition Modeling (FDM / FFF)", "c": "Stereolithography (SLA)", "d": "Direct Metal Laser Sintering (DMLS)"},
                        "answer": "b",
                    },
                ],
            },
        ],
    },
    "MCA": {
        "domain_name": "Master of Computer Applications (MCA)",
        "domain_icon": "📱",
        "target_domain": "MCA",
        "target_department": "Computer Applications",
        "exams": [
            {
                "title": "MCA-101: Enterprise Java & Spring Framework",
                "description": "Spring Boot, REST controllers, Hibernate/JPA entity mapping, and JVM memory model.",
                "duration_minutes": 45,
                "total_questions": 5,
                "target_domain": "MCA",
                "target_department": "Computer Applications",
                "target_year": "All",
                "target_status": "All",
                "questions": [
                    {
                        "id": 1,
                        "text": "In Spring Boot, which annotation marks a class as an HTTP REST endpoint controller?",
                        "options": {"a": "@Entity", "b": "@RestController", "c": "@Repository", "d": "@Service"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "Which JVM memory area stores class metadata, runtime constant pool, and method bytecodes?",
                        "options": {"a": "Heap Space", "b": "Metaspace / Method Area", "c": "Thread Stack", "d": "Program Counter"},
                        "answer": "b",
                    },
                    {
                        "id": 3,
                        "text": "In JPA / Hibernate, which annotation defines a Many-to-One relationship between entities?",
                        "options": {"a": "@OneToOne", "b": "@ManyToOne", "c": "@ManyToMany", "d": "@JoinColumnOnly"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "What core design principle is implemented by Spring IoC Container for object lifecycle?",
                        "options": {"a": "Dependency Injection (Inversion of Control)", "b": "Active Record Pattern", "c": "Flyweight caching", "d": "Chain of Responsibility"},
                        "answer": "a",
                    },
                    {
                        "id": 5,
                        "text": "Which modern Java Garbage Collector is designed for low pause times on large heaps?",
                        "options": {"a": "Serial GC", "b": "G1 (Garbage-First) GC", "c": "Epsilon No-Op GC", "d": "Copying Collector"},
                        "answer": "b",
                    },
                ],
            },
            {
                "title": "MCA-102: Object Oriented Software Engineering & Design Patterns",
                "description": "Gang of Four design patterns, SOLID principles, UML modeling, and architectural styles.",
                "duration_minutes": 45,
                "total_questions": 5,
                "target_domain": "MCA",
                "target_department": "Computer Applications",
                "target_year": "All",
                "target_status": "All",
                "questions": [
                    {
                        "id": 1,
                        "text": "Which GoF design pattern guarantees that a class has only a single instance with global access?",
                        "options": {"a": "Factory Method", "b": "Singleton Pattern", "c": "Prototype", "d": "Builder"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "In SOLID architectural principles, what does the 'L' specifically stand for?",
                        "options": {"a": "Layered Cohesion", "b": "Liskov Substitution Principle", "c": "Lazy Initialization", "d": "Linear Inheritance"},
                        "answer": "b",
                    },
                    {
                        "id": 3,
                        "text": "In UML class diagrams, what relationship does a solid filled diamond represent?",
                        "options": {"a": "Aggregation (weak ownership)", "b": "Composition (strong ownership)", "c": "Generalization", "d": "Interface Realization"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "Which structural pattern attaches new responsibilities dynamically without subclassing?",
                        "options": {"a": "Decorator Pattern", "b": "Adapter Pattern", "c": "Facade Pattern", "d": "Bridge Pattern"},
                        "answer": "a",
                    },
                    {
                        "id": 5,
                        "text": "Which design pattern provides a unified, simplified interface to a complex subsystem of classes?",
                        "options": {"a": "Proxy", "b": "Facade Pattern", "c": "Flyweight", "d": "Interpreter"},
                        "answer": "b",
                    },
                ],
            },
            {
                "title": "MCA-103: Cloud Computing & Virtualization Architecture",
                "description": "Cloud service models (IaaS/PaaS/SaaS), hypervisors, Docker containers, and Kubernetes orchestration.",
                "duration_minutes": 45,
                "total_questions": 5,
                "target_domain": "MCA",
                "target_department": "Computer Applications",
                "target_year": "All",
                "target_status": "All",
                "questions": [
                    {
                        "id": 1,
                        "text": "Which cloud model provides raw virtualized machines, storage, and networking for customer configuration?",
                        "options": {"a": "SaaS", "b": "PaaS", "c": "IaaS (Infrastructure as a Service)", "d": "FaaS"},
                        "answer": "c",
                    },
                    {
                        "id": 2,
                        "text": "What characterizes a Type-1 (Bare-Metal) hypervisor like VMware ESXi or Xen?",
                        "options": {"a": "Runs directly on the bare host hardware without an underlying OS", "b": "Runs as an application inside Windows", "c": "Requires Docker to execute", "d": "Only executes Python code"},
                        "answer": "a",
                    },
                    {
                        "id": 3,
                        "text": "Which Linux kernel primitives form the core foundation of Docker container isolation?",
                        "options": {"a": "Namespaces and cgroups", "b": "FAT32 file system", "c": "Systemd services only", "d": "Swap partitions"},
                        "answer": "a",
                    },
                    {
                        "id": 4,
                        "text": "In AWS cloud services, what product provides serverless event-driven function execution?",
                        "options": {"a": "EC2 Instances", "b": "AWS Lambda", "c": "Amazon EBS", "d": "Amazon S3"},
                        "answer": "b",
                    },
                    {
                        "id": 5,
                        "text": "In Kubernetes, what is the smallest atomic deployable execution unit containing one or more containers?",
                        "options": {"a": "Node", "b": "Pod", "c": "Cluster", "d": "Ingress"},
                        "answer": "b",
                    },
                ],
            },
            {
                "title": "MCA-104: Python & Full Stack Web Architecture",
                "description": "Python OOP, asynchronous programming (asyncio), Django MVT, and REST API conventions.",
                "duration_minutes": 45,
                "total_questions": 5,
                "target_domain": "MCA",
                "target_department": "Computer Applications",
                "target_year": "All",
                "target_status": "All",
                "questions": [
                    {
                        "id": 1,
                        "text": "In Python, which decorator defines a method bound to the class rather than an instance?",
                        "options": {"a": "@staticmethod", "b": "@classmethod", "c": "@property", "d": "@wrapper"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "In the Django web framework, what architectural acronym describes its pattern?",
                        "options": {"a": "MVT (Model-View-Template)", "b": "CQRS", "c": "Event Sourcing", "d": "Clean Onion"},
                        "answer": "a",
                    },
                    {
                        "id": 3,
                        "text": "In modern asynchronous Python (asyncio), which keyword suspends coroutine execution until completion?",
                        "options": {"a": "yield", "b": "await", "c": "defer", "d": "pause"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "Which HTTP status code signifies that a new resource was successfully created on the server?",
                        "options": {"a": "200 OK", "b": "201 Created", "c": "204 No Content", "d": "302 Found"},
                        "answer": "b",
                    },
                    {
                        "id": 5,
                        "text": "Which lightweight data interchange format is native to JavaScript and standard across REST APIs?",
                        "options": {"a": "XML", "b": "JSON", "c": "YAML", "d": "Protocol Buffers"},
                        "answer": "b",
                    },
                ],
            },
            {
                "title": "MCA-105: Advanced Data Structures & Algorithm Optimization",
                "description": "Self-balancing trees, dynamic programming, greedy algorithms, and graph optimizations.",
                "duration_minutes": 45,
                "total_questions": 5,
                "target_domain": "MCA",
                "target_department": "Computer Applications",
                "target_year": "All",
                "target_status": "All",
                "questions": [
                    {
                        "id": 1,
                        "text": "What is the worst-case lookup time complexity in a balanced Red-Black Tree with n keys?",
                        "options": {"a": "O(1)", "b": "O(log n)", "c": "O(n)", "d": "O(n log n)"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "Which design paradigm is the fundamental core of Dijkstra's single-source shortest path algorithm?",
                        "options": {"a": "Greedy Paradigm", "b": "Dynamic Programming", "c": "Divide and Conquer", "d": "Branch and Bound"},
                        "answer": "a",
                    },
                    {
                        "id": 3,
                        "text": "What is the maximum auxiliary stack memory consumed during DFS on a tree of height h?",
                        "options": {"a": "O(1)", "b": "O(h)", "c": "O(2^h)", "d": "O(h²)"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "Which data structure guarantees extracting the minimum or maximum element in O(1) time?",
                        "options": {"a": "Binary Heap (Priority Queue)", "b": "Circular Linked List", "c": "Unordered Hash Set", "d": "Trie"},
                        "answer": "a",
                    },
                    {
                        "id": 5,
                        "text": "What key property distinguishes Dynamic Programming from standard divide-and-conquer recursion?",
                        "options": {"a": "Overlapping subproblems solved once via memoization or tabulation", "b": "Random pivot splitting", "c": "Linear scan search", "d": "Immediate heuristic choice"},
                        "answer": "a",
                    },
                ],
            },
        ],
    },
    "BA": {
        "domain_name": "Bachelor of Arts (BA Humanities & Social Sciences)",
        "domain_icon": "📚",
        "target_domain": "BA",
        "target_department": "Humanities / Arts",
        "exams": [
            {
                "title": "BA-101: Modern English Literature & Critical Theory",
                "description": "Literary theory, modern prose, narrative structures, and historical literary movements.",
                "duration_minutes": 45,
                "total_questions": 5,
                "target_domain": "BA",
                "target_department": "English Literature",
                "target_year": "All",
                "target_status": "All",
                "questions": [
                    {
                        "id": 1,
                        "text": "Who composed the landmark modernist poem 'The Waste Land' published in 1922?",
                        "options": {"a": "W.B. Yeats", "b": "T.S. Eliot", "c": "Ezra Pound", "d": "Virginia Woolf"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "Which critical literary school analyzes literature primarily through socio-economic and class conflict lenses?",
                        "options": {"a": "New Criticism", "b": "Marxist Literary Criticism", "c": "Deconstruction", "d": "Formalism"},
                        "answer": "b",
                    },
                    {
                        "id": 3,
                        "text": "Which literary technique replicates the continuous, unfiltered flow of conscious thoughts in prose?",
                        "options": {"a": "Stream of Consciousness", "b": "Allegorical Didacticism", "c": "Epistolary framing", "d": "Dramatic Irony"},
                        "answer": "a",
                    },
                    {
                        "id": 4,
                        "text": "In classical dramatic theory (Aristotle), what term denotes the emotional purgation experienced by spectators?",
                        "options": {"a": "Hamartia", "b": "Catharsis", "c": "Anagnorisis", "d": "Peripeteia"},
                        "answer": "b",
                    },
                    {
                        "id": 5,
                        "text": "Which celebrated author penned the classics 'Pride and Prejudice' and 'Sense and Sensibility'?",
                        "options": {"a": "Charlotte Brontë", "b": "Jane Austen", "c": "George Eliot", "d": "Emily Dickinson"},
                        "answer": "b",
                    },
                ],
            },
            {
                "title": "BA-102: Principles of Micro & Macro Economics",
                "description": "Supply and demand, market equilibrium, fiscal and monetary policies, and macroeconomic metrics.",
                "duration_minutes": 45,
                "total_questions": 5,
                "target_domain": "BA",
                "target_department": "Economics",
                "target_year": "All",
                "target_status": "All",
                "questions": [
                    {
                        "id": 1,
                        "text": "When consumer demand for a normal product rises while supply remains fixed, what is the impact on price?",
                        "options": {"a": "Equilibrium price falls", "b": "Equilibrium price rises", "c": "Price is unaffected", "d": "Supply shifts to zero"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "Which macroeconomic metric represents the total market value of all finished goods produced within a country in a year?",
                        "options": {"a": "Consumer Price Index (CPI)", "b": "Gross Domestic Product (GDP)", "c": "Balance of Payments", "d": "Net Foreign Remittance"},
                        "answer": "b",
                    },
                    {
                        "id": 3,
                        "text": "What market structure describes an industry controlled by a small handful of large competing firms?",
                        "options": {"a": "Pure Monopoly", "b": "Oligopoly", "c": "Monopsony", "d": "Perfect Competition"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "What is the primary macroeconomic purpose when a central bank raises its benchmark policy interest rates?",
                        "options": {"a": "Accelerate consumer borrowing", "b": "Combat inflation and reduce overheated demand", "c": "Depreciate the currency", "d": "Encourage budget deficits"},
                        "answer": "b",
                    },
                    {
                        "id": 5,
                        "text": "What fundamental economic concept represents the value of the next best alternative foregone?",
                        "options": {"a": "Marginal Sunk Cost", "b": "Opportunity Cost", "c": "Fixed Capital Cost", "d": "Depreciation Expense"},
                        "answer": "b",
                    },
                ],
            },
            {
                "title": "BA-103: Political Systems & Constitutional Governance",
                "description": "Constitutional law, democratic institutions, political theories, and governance structures.",
                "duration_minutes": 45,
                "total_questions": 5,
                "target_domain": "BA",
                "target_department": "Political Science",
                "target_year": "All",
                "target_status": "All",
                "questions": [
                    {
                        "id": 1,
                        "text": "Which article of the Indian Constitution grants the Right to Constitutional Remedies (calling it heart and soul)?",
                        "options": {"a": "Article 14", "b": "Article 19", "c": "Article 21", "d": "Article 32"},
                        "answer": "d",
                    },
                    {
                        "id": 2,
                        "text": "Who authored the 1651 political treatise 'Leviathan' establishing social contract theory and sovereign authority?",
                        "options": {"a": "John Locke", "b": "Thomas Hobbes", "c": "Jean-Jacques Rousseau", "d": "Montesquieu"},
                        "answer": "b",
                    },
                    {
                        "id": 3,
                        "text": "Which constitutional doctrine prevents tyranny by distributing power across legislative, executive, and judicial organs?",
                        "options": {"a": "Rule of Ordinance", "b": "Separation of Powers", "c": "Judicial Precedence", "d": "Unitary Hegemony"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "In parliamentary democracy, who holds de facto chief executive power over state governance?",
                        "options": {"a": "The Monarch / Head of State", "b": "The Prime Minister & Cabinet", "c": "The Chief Justice", "d": "The Military Council"},
                        "answer": "b",
                    },
                    {
                        "id": 5,
                        "text": "Under the 61st Constitutional Amendment Act in India, what is the universal minimum voting age?",
                        "options": {"a": "21 years", "b": "18 years", "c": "20 years", "d": "25 years"},
                        "answer": "b",
                    },
                ],
            },
            {
                "title": "BA-104: World History, Civilizations & Modern Societies",
                "description": "Ancient world civilizations, the European Renaissance, democratic revolutions, and global conflicts.",
                "duration_minutes": 45,
                "total_questions": 5,
                "target_domain": "BA",
                "target_department": "History",
                "target_year": "All",
                "target_status": "All",
                "questions": [
                    {
                        "id": 1,
                        "text": "Which ancient civilization developed along the Nile River and constructed the Pyramids of Giza?",
                        "options": {"a": "Mesopotamian", "b": "Ancient Egyptian Civilization", "c": "Indus Valley", "d": "Phoenician"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "The storming of which royal fortress on July 14, 1789 ignited the French Revolution?",
                        "options": {"a": "Palace of Versailles", "b": "Bastille Fortress", "c": "Tuileries Palace", "d": "Château de Vincennes"},
                        "answer": "b",
                    },
                    {
                        "id": 3,
                        "text": "Which worldwide intergovernmental body was established in 1945 directly following World War II?",
                        "options": {"a": "League of Nations", "b": "United Nations (UN)", "c": "Warsaw Treaty Organization", "d": "European Coal and Steel Community"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "Which mid-15th century invention by Johannes Gutenberg revolutionized mass literacy and knowledge dissemination?",
                        "options": {"a": "Movable-type printing press", "b": "Mechanical clockwork", "c": "Astronomical quadrant", "d": "Steam turbine"},
                        "answer": "a",
                    },
                    {
                        "id": 5,
                        "text": "Which European city and region is recognized as the cradle of the Renaissance in the 14th century?",
                        "options": {"a": "Paris, France", "b": "Florence, Italy", "c": "London, England", "d": "Madrid, Spain"},
                        "answer": "b",
                    },
                ],
            },
            {
                "title": "BA-105: Foundations of Human Psychology & Cognitive Behavior",
                "description": "Cognitive psychology, behavioral conditioning, psychological development, and brain structures.",
                "duration_minutes": 45,
                "total_questions": 5,
                "target_domain": "BA",
                "target_department": "Psychology",
                "target_year": "All",
                "target_status": "All",
                "questions": [
                    {
                        "id": 1,
                        "text": "Who established the foundation of psychoanalytic psychology proposing the id, ego, and superego?",
                        "options": {"a": "B.F. Skinner", "b": "Sigmund Freud", "c": "Carl Rogers", "d": "Jean Piaget"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "In Ivan Pavlov's classical conditioning experiments, what served as the unconditioned stimulus?",
                        "options": {"a": "Sound of the metronome/bell", "b": "Presentation of food powder", "c": "Lab technician's footsteps", "d": "Salivary response"},
                        "answer": "b",
                    },
                    {
                        "id": 3,
                        "text": "Which limbic system brain structure is essential for long-term memory encoding and spatial awareness?",
                        "options": {"a": "Medulla Oblongata", "b": "Hippocampus", "c": "Occipital Cortex", "d": "Pons"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "In Maslow's Hierarchy of Needs, what tier sits at the pinnacle of human psychological potential?",
                        "options": {"a": "Social Belonging", "b": "Self-Actualization", "c": "Safety and Shelter", "d": "Esteem and Prestige"},
                        "answer": "b",
                    },
                    {
                        "id": 5,
                        "text": "Which systematic cognitive bias leads individuals to selectively embrace evidence validating existing beliefs?",
                        "options": {"a": "Hindsight bias", "b": "Confirmation bias", "c": "Halo effect", "d": "Anchoring heuristic"},
                        "answer": "b",
                    },
                ],
            },
        ],
    },
    "General": {
        "domain_name": "General Aptitude & Foundation (Open to All / Beginners)",
        "domain_icon": "🌟",
        "target_domain": "All",
        "target_department": "All",
        "exams": [
            {
                "title": "GEN-101: Quantitative Aptitude & Analytical Reasoning",
                "description": "Mathematical problem solving, percentage calculations, time and work, and number series.",
                "duration_minutes": 30,
                "total_questions": 5,
                "target_domain": "All",
                "target_department": "All",
                "target_year": "All",
                "target_status": "All",
                "questions": [
                    {
                        "id": 1,
                        "text": "If a train traveling at 60 km/h passes a 150-meter-long platform in 18 seconds, what is the train's length?",
                        "options": {"a": "120 meters", "b": "150 meters", "c": "180 meters", "d": "200 meters"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "What is the logical next number in the geometric progression: 3, 7, 15, 31, 63, ...?",
                        "options": {"a": "125", "b": "127", "c": "128", "d": "130"},
                        "answer": "b",
                    },
                    {
                        "id": 3,
                        "text": "If 12 workers finish a project in 10 days, how many days will 15 workers require at the same pace?",
                        "options": {"a": "6 days", "b": "8 days", "c": "11 days", "d": "12 days"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "The ratio of boys to girls in a class of 45 students is 3:2. How many girls are enrolled?",
                        "options": {"a": "18 girls", "b": "20 girls", "c": "25 girls", "d": "27 girls"},
                        "answer": "a",
                    },
                    {
                        "id": 5,
                        "text": "A retailer sells an article for $480 incurring a 20% loss on cost price. What was the original cost?",
                        "options": {"a": "$550", "b": "$600", "c": "$580", "d": "$620"},
                        "answer": "b",
                    },
                ],
            },
            {
                "title": "GEN-102: Computer Basics & Digital Literacy",
                "description": "Hardware architecture basics, file management, internet security, and digital productivity tools.",
                "duration_minutes": 30,
                "total_questions": 5,
                "target_domain": "All",
                "target_department": "All",
                "target_year": "All",
                "target_status": "All",
                "questions": [
                    {
                        "id": 1,
                        "text": "Which hardware unit coordinates data processing and is termed the 'brain' of the computer?",
                        "options": {"a": "Random Access Memory", "b": "Central Processing Unit (CPU)", "c": "Solid State Drive", "d": "Graphics Processing Unit"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "What universal operating system keyboard shortcut reverts the most recent user action?",
                        "options": {"a": "Ctrl + C", "b": "Ctrl + Z", "c": "Ctrl + Y", "d": "Ctrl + X"},
                        "answer": "b",
                    },
                    {
                        "id": 3,
                        "text": "What does the 'S' designate in the secure web protocol 'HTTPS'?",
                        "options": {"a": "Speed", "b": "Secure (Encrypted SSL/TLS connection)", "c": "Standard", "d": "Shared"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "How many Megabytes (MB) constitute exactly 1 Gigabyte (GB) in standard digital storage?",
                        "options": {"a": "100 MB", "b": "1024 MB", "c": "512 MB", "d": "2048 MB"},
                        "answer": "b",
                    },
                    {
                        "id": 5,
                        "text": "What is the primary function of dedicated endpoint antivirus software?",
                        "options": {"a": "Boost internet bandwidth", "b": "Detect, quarantine, and eliminate malware and viruses", "c": "Defragment hard drives automatically", "d": "Overclock system clock frequencies"},
                        "answer": "b",
                    },
                ],
            },
            {
                "title": "GEN-103: Professional Workplace Communication & Ethics",
                "description": "Business etiquette, active listening, conflict resolution, confidentiality, and professional integrity.",
                "duration_minutes": 30,
                "total_questions": 5,
                "target_domain": "All",
                "target_department": "All",
                "target_year": "All",
                "target_status": "All",
                "questions": [
                    {
                        "id": 1,
                        "text": "Which communication component provides confirmation that the recipient accurately understood the message?",
                        "options": {"a": "Transmission medium", "b": "Feedback", "c": "Encoding buffer", "d": "Atmospheric noise"},
                        "answer": "b",
                    },
                    {
                        "id": 2,
                        "text": "In business email etiquette, which field sends a copy to an individual without revealing their identity to others?",
                        "options": {"a": "To field", "b": "Cc (Carbon Copy)", "c": "Bcc (Blind Carbon Copy)", "d": "Subject Line"},
                        "answer": "c",
                    },
                    {
                        "id": 3,
                        "text": "Which habit demonstrates effective active listening during high-stakes professional meetings?",
                        "options": {"a": "Interrupting immediately to correct points", "b": "Paying focused attention, taking notes, and validating before answering", "c": "Checking mobile devices silently", "d": "Formulating rebuttals while the speaker talks"},
                        "answer": "b",
                    },
                    {
                        "id": 4,
                        "text": "What core ethical standard obligates professionals to safeguard confidential organizational information?",
                        "options": {"a": "Commercialization", "b": "Confidentiality & Non-Disclosure", "c": "Open Source Sharing", "d": "Publicity Rights"},
                        "answer": "b",
                    },
                    {
                        "id": 5,
                        "text": "Which communication posture is most constructive for resolving workplace project disagreements?",
                        "options": {"a": "Aggressive and uncompromising", "b": "Calm, empathetic, and solution-focused", "c": "Passive and detached", "d": "Sarcastic"},
                        "answer": "b",
                    },
                ],
            },
        ],
    },
}


def get_all_catalog_exams():
    """Flatten all exams across domains into a single list with target eligibility info."""
    flattened = []
    for domain_key, domain_data in DOMAIN_CATALOG.items():
        domain_default = domain_data.get("target_domain", "B.Tech")
        dept_default = domain_data.get("target_department", domain_key)
        for exam in domain_data["exams"]:
            exam_copy = dict(exam)
            exam_copy["subject"] = domain_key
            exam_copy["domain_name"] = domain_data["domain_name"]
            exam_copy["domain_icon"] = domain_data["domain_icon"]
            exam_copy["target_domain"] = exam.get("target_domain", domain_default)
            exam_copy["target_department"] = exam.get("target_department", dept_default)
            exam_copy["target_year"] = exam.get("target_year", "All")
            exam_copy["target_status"] = exam.get("target_status", "All")
            flattened.append(exam_copy)
    return flattened


def get_exam_questions(exam_title):
    """
    Retrieve the 5 curated questions for a given exam title.
    Falls back to first matching exam or a default set if not found.
    """
    title_clean = (exam_title or "").strip().lower()
    for domain_key, domain_data in DOMAIN_CATALOG.items():
        for ex in domain_data["exams"]:
            if ex["title"].lower() in title_clean or title_clean in ex["title"].lower():
                return ex["questions"]

    # Fallback to CSE-101 questions
    return DOMAIN_CATALOG["CSE"]["exams"][0]["questions"]


def grade_exam(exam_title, submitted_answers):
    """
    Calculate score given candidate's submitted answers.
    submitted_answers: dict e.g. {'q1': 'b', 'q2': 'a', ...}
    Returns dict: {'score': 4, 'total': 5, 'percentage': 80.0, 'results': [...]}
    """
    questions = get_exam_questions(exam_title)
    correct_count = 0
    results = []

    for q in questions:
        q_key = f"q{q['id']}"
        cand_ans = (submitted_answers.get(q_key) or "").strip().lower()
        is_correct = (cand_ans == q["answer"].lower())
        if is_correct:
            correct_count += 1
        results.append({
            "id": q["id"],
            "question": q["text"],
            "candidate_answer": cand_ans.upper() if cand_ans else "Not Answered",
            "correct_answer": q["answer"].upper(),
            "is_correct": is_correct,
        })

    total = len(questions)
    pct = round((correct_count / total) * 100, 1) if total > 0 else 0.0

    return {
        "score": correct_count,
        "total": total,
        "percentage": pct,
        "score_str": f"{correct_count}/{total} ({pct}%)",
        "passed": pct >= 40.0,
        "results": results,
    }


def seed_domain_catalog():
    """
    Seed or update all domain assessments in the database.
    Ensures that every domain has its active tests with target eligibility fields.
    """
    existing_titles = {e.title: e for e in AvailableExam.query.all()}
    count_added = 0

    for exam_info in get_all_catalog_exams():
        title = exam_info["title"]
        if title not in existing_titles:
            new_exam = AvailableExam(
                title=title,
                description=exam_info["description"],
                duration_minutes=exam_info["duration_minutes"],
                total_questions=exam_info["total_questions"],
                subject=exam_info["subject"],
                target_domain=exam_info.get("target_domain", "All"),
                target_department=exam_info.get("target_department", "All"),
                target_year=exam_info.get("target_year", "All"),
                target_status=exam_info.get("target_status", "All"),
                is_active=True,
            )
            db.session.add(new_exam)
            count_added += 1
        else:
            ex = existing_titles[title]
            ex.subject = exam_info["subject"]
            ex.total_questions = exam_info["total_questions"]
            ex.description = exam_info["description"]
            ex.target_domain = exam_info.get("target_domain", "All")
            ex.target_department = exam_info.get("target_department", "All")
            ex.target_year = exam_info.get("target_year", "All")
            ex.target_status = exam_info.get("target_status", "All")
            ex.is_active = True

    db.session.commit()
    return count_added

