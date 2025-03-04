import sys
sys.path.append('D:/Code/Label_software/FastSAM-main')
import os
from PIL import Image, ImageDraw
import pandas as pd
from PySide6 import QtWidgets, QtGui
from PySide6.QtWidgets import QFileDialog, QMessageBox, QLabel, QRadioButton, QVBoxLayout, QHBoxLayout, QGroupBox, QPushButton, QMainWindow, QWidget, QLineEdit, QFormLayout, QSplitter, QGridLayout, QTextEdit, QSizePolicy, QInputDialog, QMessageBox
from PySide6.QtGui import QPixmap, QMouseEvent, QPainter
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PIL import Image
import re
import cv2
from fastsam.model import FastSAM
from prompt import FastSAMPrompt
import matplotlib.pyplot as plt
import numpy as np
#计算每个轮廓的x和y的最大值和最小值
import numpy as np
import pandas as pd
def find_min_max(nested_list):
    # 用于存储每个下标的x和y的最大、最小值
    result = []
    
    for sublist in nested_list:
        # 提取所有 x 和 y 值
        x_values = [point[0] for contour in sublist for point in contour]
        y_values = [point[1] for contour in sublist for point in contour]

        # 计算 x 和 y 的最小值和最大值
        x_min, x_max = min(x_values), max(x_values)
        y_min, y_max = min(y_values), max(y_values)
        
        # 添加结果到列表
        result.append({
            "x_min": x_min,
            "x_max": x_max,
            "y_min": y_min,
            "y_max": y_max
        })
    
    return result

def find_index_of_coordinate(nested_list,x, y):

    results = find_min_max(nested_list)
    for i, value in enumerate(results):
        x_min = value['x_min']
        x_max = value['x_max']
        y_min = value['y_min']
        y_max = value['y_max']
        if x_min <= x <= x_max and y_min <= y <= y_max:
            return i, results
    return -1, None  # 如果未找到返回 -1


class DataCollector:
    def __init__(self):
        # 实例变量 DataFrame
        self.data = pd.DataFrame(columns=["x_min", "x_max", "y_min", "y_max"])

    def add_data(self, x_min, x_max, y_min, y_max):
        # 新行数据
        new_row = pd.DataFrame({"x_min": [x_min], "x_max": [x_max], "y_min": [y_min], "y_max": [y_max]})
        # 使用 pd.concat 添加新行
        self.data = pd.concat([self.data, new_row], ignore_index=True)

class ImageLabelingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Annotation software for human assembly intention recognition')
        # self.setFixedSize(1200, 800) 
        self.showMaximized()
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setWindowIcon(QIcon("FastSAM-main/icon.jpg"))
        # 标签和文件列表
        self.label_groups = {}
        self.label_groups_ui = {}  # 初始化 label_groups_ui
        self.label_vars = {}  # 初始化 label_vars
        self.image_files = []
        self.current_image_index = 0
        self.annotations = []
        self.load_categories_from_excel("D:/Code/Label_software/obejct_label.xlsx")
        
        # 标签编号计数，每个标签组独立
        self.label_counters = {}
        
        # 默认保存路径
        # self.save_path = "annotations.txt"
        # self.save_path_object_detection = "annotation_objection _detection.txt"
        
        # 加载 FastSAM 模型
        self.model = FastSAM('FastSAM-x.pt')
        
        # 界面组件
        self.init_ui()
        #选中物体组件
        self.selected_contonur = None
        # self.contours = []
        self.currnt_image_index = 0
        # self.image_files = []


    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建一个垂直的主布局
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # 创建上方的水平布局，包括左侧的垂直功能按钮区域和图片显示区
        top_layout = QHBoxLayout()
        main_layout.addLayout(top_layout)

        # 创建左侧的垂直功能按钮区域
        control_widget = QWidget()
        control_layout = QVBoxLayout(control_widget)
        control_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)

        # 添加功能按钮到左侧布局
        self.add_group_button = QPushButton('Labels')
        self.add_group_button.clicked.connect(self.choose_label_group_method)
        control_layout.addWidget(self.add_group_button)

     # 添加功能按钮到左侧布局
        # self.add_object_detection_group_button = QPushButton('目标检测标签')
        # self.add_object_detection_group_button.clicked.connect(self.choose_object_label_group_method)
        # control_layout.addWidget(self.add_object_detection_group_button)

        # self.load_images_button = QPushButton('加载数据')
        # self.load_images_button.clicked.connect(self.load_images)
        # control_layout.addWidget(self.load_images_button)

        # 将左侧功能区添加到上方布局
        top_layout.addWidget(control_widget)

        # 创建图片显示区并添加到上方布局
        self.image_label = QLabel()
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setStyleSheet("background-color: lightgray;")
        self.image_label.mousePressEvent = self.label_image
        top_layout.addWidget(self.image_label)

        # 初始化标签布局
        self.label_layout = QVBoxLayout()
        control_layout.addLayout(self.label_layout)

        # 创建下方的控制按钮区域
        bottom_layout = QHBoxLayout()
        main_layout.addLayout(bottom_layout)

        self.set_save_path_button = QPushButton('save path')
        self.set_save_path_button.clicked.connect(self.set_save_path)
        bottom_layout.addWidget(self.set_save_path_button)

        self.segment_anything_button = QPushButton('segment')
        self.segment_anything_button.clicked.connect(self.segment_anything)
        bottom_layout.addWidget(self.segment_anything_button)

        self.prev_button = QPushButton('previsou')
        self.prev_button.clicked.connect(self.prev_image)
        bottom_layout.addWidget(self.prev_button)

        self.next_button = QPushButton('next')
        self.next_button.clicked.connect(self.next_image)
        bottom_layout.addWidget(self.next_button)


        self.load_images_button = QPushButton('data load')
        self.load_images_button.clicked.connect(self.load_images)
        bottom_layout.addWidget(self.load_images_button)

        self.save_button = QPushButton('label save')
        self.save_button.clicked.connect(self.save_annotation)
        bottom_layout.addWidget(self.save_button)

    # def choose_object_label_group_method(self):
    #     dialog = QtWidgets.QDialog(self)
    #     dialog.setWindowTitle('选择目标标签添加方式')
    #     layout = QVBoxLayout(dialog)

    #     manual_button = QPushButton('手动添加')
    #     manual_button.clicked.connect(lambda: self.add_object_label_group_manual(dialog))
    #     layout.addWidget(manual_button)

    #     import_button = QPushButton('从Excel文件导入')
    #     import_button.clicked.connect(lambda: self.import_object_label_group_from_excel(dialog))
    #     layout.addWidget(import_button)

    #     dialog.setLayout(layout)
    #     dialog.exec()

    def choose_label_group_method(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle('选择标签组添加方式')
        layout = QVBoxLayout(dialog)

        manual_button = QPushButton('手动添加')
        manual_button.clicked.connect(lambda: self.add_label_group_manual(dialog))
        layout.addWidget(manual_button)

        import_button = QPushButton('从Excel文件导入')
        import_button.clicked.connect(lambda: self.import_label_group_from_excel(dialog))
        layout.addWidget(import_button)

        dialog.setLayout(layout)
        dialog.exec()
#目标监测
    # def add_object_label_group_manual(self, parent_dialog):
    #     parent_dialog.accept()
    #     dialog = QtWidgets.QDialog(self)
    #     dialog.setWindowTitle('手动添加标签组')
    #     form_layout = QFormLayout(dialog)

    #     group_name_input = QLineEdit()
    #     label_names_input = QLineEdit()

    #     form_layout.addRow('标签名称:', group_name_input)
    #     form_layout.addRow('标签数字标识:', label_names_input)

    #     add_button = QPushButton('添加')
    #     add_button.clicked.connect(lambda: self.save_new_label_group(dialog, group_name_input.text(), label_names_input.text()))
    #     form_layout.addWidget(add_button)

    #     dialog.setLayout(form_layout)
    #     dialog.exec()

    def add_label_group_manual(self, parent_dialog):
        parent_dialog.accept()
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle('手动添加标签组')
        form_layout = QFormLayout(dialog)

        group_name_input = QLineEdit()
        label_names_input = QLineEdit()

        form_layout.addRow('标签组名称:', group_name_input)
        form_layout.addRow('标签:', label_names_input)

        add_button = QPushButton('添加')
        add_button.clicked.connect(lambda: self.save_new_label_group(dialog, group_name_input.text(), label_names_input.text()))
        form_layout.addWidget(add_button)

        dialog.setLayout(form_layout)
        dialog.exec()
        #目标检测
    # def import_object_label_group_from_excel(self, parent_dialog):
    #     parent_dialog.accept()
    #     file_path, _ = QFileDialog.getOpenFileName(self, '选择Excel文件', '', 'Excel Files (*.xlsx *.xls)')
    #     if file_path:
    #         try:
    #             df = pd.read_excel(file_path)
    #             for group_name in df.columns:
    #                 labels = df[group_name].dropna().tolist()
    #                 labels = [str(label).strip() for label in labels]
    #                 self.save_new_label_group(None, group_name, ','.join(labels))
    #         except Exception as e:
    #             QMessageBox.critical(self, '错误', f'无法导入Excel文件: {e}')

    def import_label_group_from_excel(self, parent_dialog):
        parent_dialog.accept()
        file_path, _ = QFileDialog.getOpenFileName(self, '选择Excel文件', '', 'Excel Files (*.xlsx *.xls)')
        if file_path:
            try:
                df = pd.read_excel(file_path)
                for group_name in df.columns:
                    labels = df[group_name].dropna().tolist()
                    labels = [str(label).strip() for label in labels]
                    self.save_new_label_group(None, group_name, ','.join(labels))
            except Exception as e:
                QMessageBox.critical(self, '错误', f'无法导入Excel文件: {e}')
#目标检测结果存储

    def save_new_label_group(self, dialog, group_name, label_names):
        if not group_name or not label_names:
            QMessageBox.critical(self, '错误', '标签组名称和标签不能为空')
            return
        labels = label_names.split(',')
        labels = [label.strip() for label in labels]

        # 初始化标签组编号计数器
        if group_name not in self.label_counters:
            self.label_counters[group_name] = 0

        # 解析标签，给每个标签分配唯一的数字标记（每个标签组独立编号）
        parsed_labels = {}
        for label in labels:
            key = re.sub(r'\s+', '', label.lower())  # 去除空格，转为小写
            parsed_labels[key] = str(self.label_counters[group_name] % 11)  # 0-10之间的数字循环
            self.label_counters[group_name] += 1

        if group_name in self.label_groups:
            # 如果标签组已存在，添加新的标签
            existing_labels = set(self.label_groups[group_name].keys())
            new_labels = {k: v for k, v in parsed_labels.items() if k not in existing_labels}
            self.label_groups[group_name].update(new_labels)
            self.update_label_group_ui(group_name, new_labels.keys())
        else:
            # 如果标签组不存在，创建新的标签组
            self.label_groups[group_name] = parsed_labels
            self.create_label_group_ui(group_name, parsed_labels.keys())
        if dialog:
            dialog.accept()

    def create_label_group_ui(self, group, labels):
        if group in self.label_groups_ui:
            group_box = self.label_groups_ui[group]
            group_layout = group_box.layout()
        else:
            # 创建新的标签组
            group_box = QGroupBox(group)
            group_layout = QVBoxLayout()
            group_box.setLayout(group_layout)
            self.label_groups_ui[group] = group_box
            self.label_layout.addWidget(group_box)
            self.label_vars[group] = {}  # 将每个标签组的标签与图片相关联
        
        # 添加新标签到标签组
        for label in labels:
            label_with_number = f"{label} ({self.label_groups[group][label]})"
            rb = QRadioButton(label_with_number)
            rb.toggled.connect(lambda checked, l=label, g=group: self.set_label_var(g, l, rb) if rb.isChecked() else None)
            group_layout.addWidget(rb)
            self.label_vars[group][label] = rb

    def update_label_group_ui(self, group, new_labels):
        # 更新已有的标签组
        group_box = self.label_groups_ui[group]
        group_layout = group_box.layout()
        for label in new_labels:
            label_with_number = f"{label} ({self.label_groups[group][label]})"
            rb = QRadioButton(label_with_number)
            rb.toggled.connect(lambda checked, l=label, g=group: self.set_label_var(g, l, rb))
            group_layout.addWidget(rb)
            self.label_vars[group][label] = rb

    def load_categories_from_excel(self, file_path):
        """从 Excel 文件加载类别"""
        try:
            df = pd.read_excel(file_path)
            self.categories = df.iloc[:, 0].dropna().tolist()  # 假设类别在第一列
        except Exception as e:
            QMessageBox.critical(self, "加载错误", f"无法加载 Excel 文件：{e}")

    def load_images(self):
        folder_path = QFileDialog.getExistingDirectory(self, '选择文件夹')
        #获取上一级目录
        self.parent_dir = os.path.dirname(folder_path)
        if folder_path:
            self.image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.jpg')]
            if not self.image_files:
                QMessageBox.critical(self, '错误', '未找到jpg图片')
                return
            self.current_image_index = 0
            self.show_image()

    def set_save_path(self):
        file_path, _ = QFileDialog.getSaveFileName(self, 'Saving file', '', 'Text Files (*.txt)')
        if file_path:
            self.save_path = file_path
            # print(f'save path:{self.save_path}')

    def show_image(self):
        if not self.image_files:
            return
        image_path = self.image_files[self.current_image_index]
        image = Image.open(image_path)
        image.thumbnail((800, 600))
        image.save('temp.jpg')
        pixmap = QPixmap('temp.jpg')
        # painter = QPainter(self)
        # painter.drawPixmap(10,10,pixmap)
        self.image_label.setPixmap(pixmap)

        # 更新每个标签组下的标签状态
        if self.current_image_index < len(self.annotations):
            current_annotation = self.annotations[self.current_image_index]
        else:
            current_annotation = {}

        for group, labels in self.label_vars.items():
            for label, rb in labels.items():
                if isinstance(rb, QRadioButton):
                    rb.setChecked(current_annotation.get(group) == label)

    def segment_anything(self):
        if not self.image_files:
            QMessageBox.critical(self, '错误', '请先加载图片')
            return
        image_path = self.image_files[self.current_image_index]
        try:
            # 使用 FastSAM 模型进行分割
            everything_results = self.model(image_path, device='cpu', retina_masks=True, imgsz=1024, conf=0.4, iou=0.9)
            prompt_process = FastSAMPrompt(image_path, everything_results, device='cpu')
            ann = prompt_process.everything_prompt()
            #self.contours是轮廓的坐标点
            self.contours = prompt_process.plot(annotations=ann, output_path='ljc.jpg')
            pixmap = QPixmap('ljc.jpg')
            self.image_label.setPixmap(pixmap)
        except Exception as e:
            QMessageBox.critical(self, '错误', f'分割失败: {e}')
    


    def prev_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.show_image()

    def next_image(self):
        if self.current_image_index < len(self.image_files) - 1:
            self.confirm_annotation()

    def confirm_annotation(self):
        # 创建一个对话框来确认标注
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle('Confirm')
        form_layout = QFormLayout(dialog)

        for group in self.label_groups:
            selected_label = next((label for label, rb in self.label_vars[group].items() if isinstance(rb, QRadioButton) and rb.isChecked() and rb.isChecked()), None)
            form_layout.addRow(f'{group}:', QLabel(selected_label if selected_label else '未标注'))

        confirm_button = QPushButton('Ok')
        confirm_button.clicked.connect(lambda: self.confirm_annotation_action(dialog))
        form_layout.addWidget(confirm_button)

        dialog.setLayout(form_layout)
        dialog.exec()

    def confirm_annotation_action(self, dialog):
        dialog.accept()
        self.save_current_annotation()
        self.current_image_index += 1
        self.show_image()

    def save_current_annotation(self):
        # 更新当前图片的标注
        if len(self.annotations) <= self.current_image_index:
            self.annotations.extend([{} for _ in range(self.current_image_index - len(self.annotations) + 1)])
        for group in self.label_groups:
            selected_label = next((label for label, rb in self.label_vars[group].items() if isinstance(rb, QRadioButton) and rb.isChecked()), None)
            self.annotations[self.current_image_index][group] = selected_label

    def label_image(self, event: QMouseEvent):
        if not self.image_files:
            return
        self.columns = ["x_min", "x_max", "y_min", "y_max"]
        self.data = pd.DataFrame(columns=self.columns)
        # 在点击的地方添加标注（示例为简单打印）
        x, y = event.pos().x(), event.pos().y()
        self.target = [x, y]
        print(f"标注位置: ({x}, {y})")
        # 可以根据需要扩展保存标注信息
        # 检查点击位置是否在某个轮廓区域内
        # print(self.contours)
        self.index, self.coords = find_index_of_coordinate(self.contours, x, y)
        if not os.path.exists(f'{self.parent_dir}/annotation'):
            os.makedirs(f'{self.parent_dir}/annotation')
        print(f"Index:{self.index}")
        #初始化dataframe用于保存数据

        if self.index != -1:
            self.save_path_object_detection = f'{self.parent_dir}/annotation/annotation_objection_detection_{self.current_image_index}.txt'
            if not os.path.exists(self.save_path_object_detection):
                with open(self.save_path_object_detection, 'w') as f:
                    #创建空文件
                    pass
            category, ok = QInputDialog.getItem(self, "", "Pick one label for object:", self.categories, 0, False)
            # print(f'category:{category}')
            if ok:
                reply = QMessageBox.question(self, "Label selection", f"是否保存类别 {category} 的标注信息？", 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    x_min = list(self.coords)[self.index]['x_min']
                    x_max = list(self.coords)[self.index]['x_max']
                    y_min = list(self.coords)[self.index]['y_min']
                    y_max = list(self.coords)[self.index]['y_max']
                    new_row = pd.DataFrame({"category":category, "x_min": [x_min], "x_max": [x_max], "y_min": [y_min], "y_max": [y_max]})
                    # 使用 pd.concat 添加新行
                    self.data = pd.concat([self.data, new_row], ignore_index=True)
                    print(self.index, list(self.coords)[self.index])
                    
                    # print(f'data:{self.data}')
                    if self.current_image_index + 1:
                        self.data.to_csv(self.save_path_object_detection, sep='\t', index=True, mode='a', header=not os.path.exists(self.save_path_object_detection))
                        self.columns = ["category", "x_min", "x_max", "y_min", "y_max"]
                        self.data = pd.DataFrame(columns=self.columns)
                        self.highlight_area(x_min, x_max, y_min, y_max)
                        QMessageBox.information(self, "信息", f"已保存类别 {category} 的标注信息")

                else:
                    QMessageBox.information(self, "警告！", "取消保存！")


                

        self.update()
    def highlight_area(self, x_min, x_max, y_min, y_max):
        # 在 QLabel 上高亮选定区域
        pixmap = self.image_label.pixmap()  # 获取当前图像
        if pixmap:
            highlighted_pixmap = pixmap.copy()  # 复制图像
            painter = QPainter(highlighted_pixmap)
            painter.setBrush(QColor(255, 0, 0, 100))  # 设置半透明红色
            painter.setPen(Qt.NoPen)  # 不显示边框
            painter.drawRect(x_min, y_min, x_max - x_min, y_max - y_min)  # 绘制高亮矩形
            painter.end()
            
        # 将高亮后的图像设置为 QLabel 的显示图像
        self.image_label.setPixmap(highlighted_pixmap)
    def point_in_contour(self, point, contour):
        # 使用 cv2.pointPolygonTest 检查点是否在轮廓内
        # `contour` 需要转换为 numpy 数组以供 `cv2` 使用
        contour_np = np.array(contour, dtype=np.int32)
        return cv2.pointPolygonTest(contour_np, point, False) >= 0    
     
    def save_annotation(self):
        if not self.image_files:
            return
        #检测文件是否存在，默认保存到与RGB一级目录
        self.save_path_action = f'{self.parent_dir}/annotation/annotation_action.txt'
        if not os.path.exists(f'{self.parent_dir}/annotation'):
            os.makedirs(f'{self.parent_dir}/annotation')
        if not os.path.exists(self.save_path_action):
             with open(self.save_path_action , 'w') as file:
                 pass
            # 保存所有图片的标注
        with open(self.save_path_action , 'w') as file:
                header = ['frame'] + list(self.label_groups.keys())
                file.write(' '.join(header) + '\n')
                for i, ann in enumerate(self.annotations):
                    annotation_line = [str(i)]
                    for group in self.label_groups:
                        label_numeric = self.label_groups[group].get(ann.get(group, "None"), "None")
                        annotation_line.append(label_numeric)
                    file.write(' '.join(annotation_line) + '\n')
        QMessageBox.information(self, '信息', '所有标注已保存')

    def set_label_var(self, group, label, rb):
        if group not in self.label_vars:
            return
        self.label_vars[group][label] = rb

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = ImageLabelingApp()
    window.show()
    app.exec()
