from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QComboBox, \
    QPushButton, QTextEdit, QShortcut, QCheckBox
from postProcessing import*
from indexing import*
import time

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setMinimumSize(800, 600)

        central_widget = QWidget()

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        toolbar_layout = QHBoxLayout()

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search...")
        toolbar_layout.addWidget(self.search_box)

        self.vector_selector = QComboBox()
        self.vector_selector.addItem("TF")
        self.vector_selector.addItem("IDF")
        self.vector_selector.addItem("TF/IDF")
        toolbar_layout.addWidget(self.vector_selector)

        self.search_type_selector = QComboBox()
        self.search_type_selector.addItem("Flat Text")
        self.search_type_selector.addItem("Structural")
        toolbar_layout.addWidget(self.search_type_selector)

        self.indexing_checkbox = QCheckBox("Indexing")
        toolbar_layout.addWidget(self.indexing_checkbox)

        self.search_btn = QPushButton("Search")
        toolbar_layout.addWidget(self.search_btn)

        main_layout.addLayout(toolbar_layout)

        self.output_text_box = QTextEdit()
        self.output_text_box.setReadOnly(True)
        main_layout.addWidget(self.output_text_box)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.enter_shortcut = QShortcut(QKeySequence(Qt.Key_Return), self)
        self.enter_shortcut.activated.connect(self.onSearch)

        self.search_btn.clicked.connect(self.onSearch)

    def onSearch(self):
        vectorList = []
        query = self.search_box.text()

        dummy_out = [

        ]

        if self.vector_selector.currentIndex() == 0 and self.search_type_selector.currentIndex() == 0 and not self.indexing_checkbox.isChecked():
            mode = "TF"
            indexing = "disabled"
            search_type = "FlatText"

            vectorList = organizeDocument(parsedTrees(documents))
            st = time.time()
            list = getKNN(vectorList,query , 5)
            en = time.time()
            print(en - st)
            dummy_out = matchIDtoDocs(list)
        elif self.vector_selector.currentIndex() == 1 and self.search_type_selector.currentIndex() == 0 and not self.indexing_checkbox.isChecked():
            mode = "IDF"
            indexing = "disabled"
            search_type = "FlatText"
            vectorList = organizeDocument(parsedTrees(documents))
            idfVectorList = getDFFlatText(vectorList)
            list = getKNN(idfVectorList,query,3)
            dummy_out = matchIDtoDocs(list)
        elif self.vector_selector.currentIndex() == 2 and self.search_type_selector.currentIndex() == 0 and not self.indexing_checkbox.isChecked():
            mode = "TF/IDF"
            indexing = "disabled"
            search_type = "FlatText"

            vectorList = organizeDocument(parsedTrees(documents))
            tfidfvectorList = getTFIDF(vectorList)
            st = time.time()
            list = getKNN(tfidfvectorList, query , 5)
            en = time.time()
            print(en-st)
            dummy_out = matchIDtoDocs(list)


        elif self.search_type_selector.currentIndex() == 1 and self.vector_selector.currentIndex() == 0 and not self.indexing_checkbox.isChecked() :
            search_type = "Structural"
            mode = "TF"
            indexing = "disabled"
            vectorList = getALlTFStruct(parsedTrees(documents))
            list = getKNNStructural(vectorList , query , 3)
            dummy_out = matchIDtoDocs(list)
        elif self.search_type_selector.currentIndex() == 1 and self.vector_selector.currentIndex() == 2  and not self.indexing_checkbox.isChecked():
            search_type = "Structural"
            mode = "TF-IDF"
            indexing = "disabled"

            vectorList = getIDFStruct(getALlTFStruct(parsedTrees(documents)))
            st = time.time()
            list = getKNNStructural(vectorList , query , 5)
            en = time.time()
            print(en-st)
            dummy_out = matchIDtoDocs(list)

        elif self.vector_selector.currentIndex() == 0 and self.search_type_selector.currentIndex() == 0 and self.indexing_checkbox.isChecked():
            indexing = "Enabled"
            mode = "TF"
            search_type = "FlatText"
            Tfvector = organizeDocument(parsedTrees(documents))
            IndexStructure = getIndexingStructure(Tfvector)
            st = time.time()
            Values = getIndexing(query, IndexStructure , Tfvector)
            list = getResultFromIndexing(Values , 5)
            en=time.time()
            print(en-st)
            dummy_out = matchIDtoDocs(list)
            print("Executed")
            print(dummy_out)

        elif self.vector_selector.currentIndex() == 1 and self.search_type_selector.currentIndex() == 0 and self.indexing_checkbox.isChecked():
            indexing = "Enabled"
            mode = "DF"
            search_type = "FlatText"
            Tfvector = organizeDocument(parsedTrees(documents))
            idfVectorList = getDFFlatText(Tfvector)
            IndexStructure = getIndexingStructure(Tfvector)
            st = time.time_ns()
            Values = getIndexing(query, IndexStructure, idfVectorList)
            list = getResultFromIndexing(Values, 5)
            en = time.time_ns()
            print(en-st)
            dummy_out = matchIDtoDocs(list)
        elif self.vector_selector.currentIndex() == 2 and self.search_type_selector.currentIndex() == 0 and self.indexing_checkbox.isChecked():
            indexing = "Enabled"
            mode = "TF-IDF"
            search_type = "FlatText"
            Tfvector = organizeDocument(parsedTrees(documents))
            TFidfVectorList = getTFIDF(Tfvector)
            IndexStructure = getIndexingStructure(Tfvector)
            Values = getIndexing(query, IndexStructure, TFidfVectorList)
            list = getResultFromIndexing(Values, 3)
            dummy_out = matchIDtoDocs(list)
        elif self.search_type_selector.currentIndex() == 1 and self.vector_selector.currentIndex() == 2 and self.indexing_checkbox.isChecked():
            print("Start")
            indexing = "Enabled"
            mode = "TF-IDF"
            search_type = "Structural"
            structIndex = getIndexingTableStruct(documents)
            print(structIndex)
            filteredDocuments = filterDocuments(query, structIndex)
            print(filteredDocuments)
            vectorList = getALlTFStruct(parsedTrees(documents))
            IDFvector = getIDFStruct(vectorList)
            st = time.time()
            list = getSimFromStruct(query, 3, filteredDocuments, IDFvector)
            en = time.time()
            print(en - st)
            dummy_out = matchIDtoDocs(list)
            print("Executed")
        else:
            dummy_out = ["Empty!"]




        output_text = f"Search results for {query} go here. \n" \
                      f"Vector Mode: {mode}. \n" \
                      f"Search Type: {search_type} \n" \
                      f"Indexing: {indexing} \n\n"
        for i, item in enumerate(dummy_out):
            output_text += f"{i+1}. {item} \n"

        self.output_text_box.setText(output_text)