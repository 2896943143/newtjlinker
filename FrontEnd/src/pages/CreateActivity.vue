<template>
  <div class="centered-container">
    <!-- 头部保持不变 -->
    <el-page-header :icon="ArrowLeft" class="header" @back="goBack">
      <template #content>
        <span class="text"> 活动创建 </span>
      </template>
    </el-page-header>
    
    <div class="large-radius">
      <div class="page-container">
        <el-form
          ref="ruleFormRef"
          :model="ruleForm"
          :rules="rules"
          label-width="auto"
          class="demo-ruleForm"
          :size="formSize"
          status-icon
          :label-position="labelPosition"
        >
          <!-- 第一行：基本信息 -->
          <el-form-item label="活动名称" prop="Name" class="form-item full-width">
            <div class="form-item-with-icon">
              <el-icon><Document /></el-icon>
              <el-input v-model="ruleForm.Name" />
            </div>
          </el-form-item>

              <el-form-item label="活动所在校区" prop="RegionKind" class="form-item">
                <div class="form-item-with-icon">
                  <el-icon><Location /></el-icon>
                  <el-select v-model="ruleForm.RegionKind" placeholder="Select">
                    <el-option label="四平路校区" value="四平路校区" />
                    <el-option label="嘉定校区" value="嘉定校区" />
                    <el-option label="沪西校区" value="沪西校区" />
                    <el-option label="沪北校区" value="沪北校区" />
                    <el-option label="校外" value="校外" />
                  </el-select>
                </div>
              </el-form-item>

              <el-form-item label="活动详细地点" prop="RegionDetailed" class="form-item">
                <div class="form-item-with-icon">
                  <el-icon><MapLocation /></el-icon>
                  <el-input v-model="ruleForm.RegionDetailed" />
                </div>
              </el-form-item>

              <el-form-item label="活动所属类目" prop="Kind" class="form-item">
                <div class="form-item-with-icon">
                  <el-icon><Folder /></el-icon>
                  <el-cascader v-model="ruleForm.Kind" :options="Options" placeholder="Select" clearable />
                </div>
              </el-form-item>

              <el-form-item label="活动时间" required="True" class="form-item">
                <div class="form-item-with-icon">
                  <el-icon><Clock /></el-icon>
                  <div class="time-picker-group">
                    <el-date-picker v-model="ruleForm.Date1" />
                    <span class="time-separator">-</span>
                    <el-time-picker v-model="ruleForm.Time1" />
                  </div>
                </div>
              </el-form-item>

              <el-form-item label="报名截止时间" required="True" class="form-item">
                <div class="form-item-with-icon">
                  <el-icon><AlarmClock /></el-icon>
                  <div class="time-picker-group">
                    <el-date-picker v-model="ruleForm.Date2" />
                    <span class="time-separator">-</span>
                    <el-time-picker v-model="ruleForm.Time2" />
                  </div>
                </div>
              </el-form-item>


          <!-- 第二行：实名互通和海报 -->
          <div class="form-row">
            <div class="form-column">
              <el-form-item label="是否期望与参与者互通实名" prop="RealName" class="form-item">
                <div class="form-item-with-icon">
                  <el-icon><User /></el-icon>
                  <el-radio-group v-model="ruleForm.RealName">
                    <el-radio value="true">是</el-radio>
                    <el-radio value="false">否</el-radio>
                  </el-radio-group>
                </div>
              </el-form-item>
              <el-form-item label="活动人数限额" prop="Num" class="form-item">
                <div class="form-item-with-icon">
                  <el-icon><UserFilled /></el-icon>
                  <el-input-number
                    v-model="ruleForm.Num"
                    :min="1"
                    :max="100"
                    @change="handleChange"
                  />
                </div>
              </el-form-item>
              <el-form-item label="活动详情" prop="Detailed" class="form-item">
                  <div class="form-item-with-icon">
                    <el-icon><Notebook /></el-icon>
                    <el-input v-model="ruleForm.Detailed" type="textarea" placeholder="请输入活动详情" rows="4" />
                  </div>
                </el-form-item>
            </div>
            
            <div class="form-column">
                  <el-form-item label="活动海报" prop="Poster" class="poster-item">
                    <!-- 这里是“活动海报”的标题 -->
                  </el-form-item>

                  <div class="poster-upload-container">
                    <!-- 这里是上传区域 -->
                    <el-upload
                      class="upload-demo"
                      action="#"
                      :auto-upload="false"
                      :on-change="handlePosterChange"
                      :show-file-list="false"
                      accept="image/*"
                    >
                      <template v-if="!posterPreview">
                        <div class="upload-area">
                          <el-icon class="upload-icon"><Upload /></el-icon>
                          <div class="upload-text">点击上传</div>
                          <div class="upload-hint">请上传活动海报图片</div>
                        </div>
                      </template>
                      <template v-else>
                        <div class="poster-preview">
                          <img :src="posterPreview" alt="海报预览"/>
                        </div>
                      </template>
                    </el-upload>
                  </div>
                </div>
          </div>


          <el-form-item class="form-buttons">
            <div class="button-container">
              <el-button type="primary" @click="submitForm(ruleFormRef)">创建</el-button>
              <el-button @click="resetForm(ruleFormRef)">重置</el-button>
            </div>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup lang='ts'>
import { ArrowLeft, Document, Location, MapLocation, Folder, 
         Clock, AlarmClock, User, UserFilled, Notebook, Upload } from '@element-plus/icons-vue'
import { reactive, ref } from "vue";
import type {
  ComponentSize,
  FormInstance,
  FormRules,
  FormProps,
} from "element-plus";
import { useRouter } from "vue-router";
const router = useRouter();

interface RuleForm {
  Creator: string;
  Name: string;
  RegionKind: string;
  RegionDetailed: string;
  Kind: string;
  Date1: string;
  Time1: string;
  Date2: string;
  Time2: string;
  RealName: boolean;
  Num: number;
  Detailed: string;
  Poster: File | null; // 新增海报文件字段
}

const formSize = ref<ComponentSize>("large");
const ruleFormRef = ref<FormInstance>();
const labelPosition = ref<FormProps["labelPosition"]>("right");
const ruleForm = reactive<RuleForm>({
  Creator: localStorage.getItem("userId") || "",
  Name: "",
  RegionKind: "",
  RegionDetailed: "",
  Kind: "",
  Date1: "",
  Time1: "",
  Date2: "",
  Time2: "",
  RealName: false,
  Num: 100,
  Detailed: "",
  Poster: null,
});
const posterPreview = ref<string | null>(null);
const handlePosterChange = (file: any) => {
  ruleForm.Poster = file.raw;
  // 生成预览图
  const reader = new FileReader();
  reader.onload = (e) => {
    posterPreview.value = e.target?.result as string;
  };
  reader.readAsDataURL(file.raw);
};


const rules = reactive<FormRules<RuleForm>>({
  Name: [
    {
      required: true,
      message: "请输入活动名称",
      trigger: "blur",
    },
    {
      validator: (rule, value, callback) => {
        if (value.length > 10) {
          callback(new Error("活动名称不能超过10个字"));
        } else {
          callback();
        }
      },
      trigger: "blur",
    },
  ],
  RegionKind: [
    {
      required: true,
      message: "请选择活动校区",
      trigger: "change",
    },
  ],
  RegionDetailed: [
    {
      required: true,
      message: "请输入活动详细地点",
      trigger: "blur",
    },
  ],
  Kind: [
    {
      required: true,
      message: "请选择活动类目",
      trigger: "change",
    },
  ],
  Date1: [
    {
      required: true,
      message: "请选择活动日期",
      trigger: "change",
    },
  ],
  Time1: [
    {
      required: true,
      message: "请选择活动时间",
      trigger: "change",
    },
  ],
  Date2: [
    {
      required: true,
      message: "请选择报名截止日期",
      trigger: "change",
    },
  ],
  Time2: [
    {
      required: true,
      message: "请选择报名截止时间",
      trigger: "change",
    },
  ],
  Detailed: [
    {
      required: true,
      message: "请输入活动详情",
      trigger: "blur",
    },
  ],
});

const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return;

  formEl.validate(async (valid, fields) => {
    if (valid) {
      const url = "http://127.0.0.1:8000/api/create_activities/";
      
      // 创建FormData对象，用于文件上传
      const formData = new FormData();
      formData.append('Name', ruleForm.Name);
      formData.append('CreatorID', ruleForm.Creator);
      formData.append('Campus_search_for_ID', ruleForm.RegionKind);
      formData.append('Location', ruleForm.RegionDetailed);
      formData.append('Class_search_for_ID1', ruleForm.Kind[0]);
      if (ruleForm.Kind[1]) {
        formData.append('Class_search_for_ID2', ruleForm.Kind[1]);
      }
      formData.append('StartDate', ruleForm.Date1 + ruleForm.Time1);
      formData.append('DueDate', ruleForm.Date2 + ruleForm.Time2);
      formData.append('NeedRealName', ruleForm.RealName.toString());
      formData.append('NumLimit', ruleForm.Num.toString());
      formData.append('Description', ruleForm.Detailed);
      
      // 如果有海报文件，添加到FormData
      if (ruleForm.Poster) {
        formData.append('poster', ruleForm.Poster);
      }

      try {
        const response = await fetch(url, {
          method: "POST",
          body: formData,  // 注意不要设置Content-Type，浏览器会自动设置
        });

        if (response.ok) {
          const data = await response.json();
          console.log("Activity created successfully:", data);
          alert("活动创建成功！");
          router.push("/home");
        } else {
          if (response.status === 405) {
            alert("报名截止时间需在活动时间之前");
          } else {
            throw new Error("活动创建失败，请稍后再试");
          }
        }
      } catch (error) {
        console.error("Error creating activity:", error);
        alert("活动创建失败，请检查表单数据并重试。");
      }
    } else {
      console.log("error submit!");
      formEl.validate();
    }
  });
};

const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.resetFields();
};

const Options = [
  {
    value: "科研竞赛",
    label: "科研竞赛",
    children: [
      {
        value: "竞赛组队",
        label: "竞赛组队",
      },
      {
        value: "项目组招募",
        label: "项目组招募",
      },
      {
        value: "其他",
        label: "其他",
      },
    ],
  },
  {
    value: "学习互助",
    label: "学习互助",
    children: [
      {
        value: "考研",
        label: "考研",
      },
      {
        value: "考公",
        label: "考公",
      },
      {
        value: "留学",
        label: "留学",
      },
      {
        value: "语言学习",
        label: "语言学习",
      },
      {
        value: "实习",
        label: "实习",
      },
      {
        value: "其他",
        label: "其他",
      },
    ],
  },
  {
    value: "体育活动",
    label: "体育活动",
    children: [
      {
        value: "羽毛球",
        label: "羽毛球",
      },
      {
        value: "乒乓球",
        label: "乒乓球",
      },
      {
        value: "网球",
        label: "网球",
      },
      {
        value: "足球",
        label: "足球",
      },
      {
        value: "排球",
        label: "排球",
      },
      {
        value: "篮球",
        label: "篮球",
      },
      {
        value: "游泳",
        label: "游泳",
      },
      {
        value: "跑步",
        label: "跑步",
      },
      {
        value: "其他",
        label: "其他",
      },
    ],
  },
  {
    value: "娱乐组局",
    label: "娱乐组局",
    children: [
      {
        value: "演唱会",
        label: "演唱会",
      },
      {
        value: "旅行",
        label: "旅行",
      },
      {
        value: "电影",
        label: "电影",
      },
      {
        value: "KTV",
        label: "KTV",
      },
      {
        value: "剧本杀",
        label: "剧本杀",
      },
      {
        value: "密室逃脱",
        label: "密室逃脱",
      },
      {
        value: "美食探店",
        label: "美食探店",
      },
      {
        value: "CityWalk",
        label: "CityWalk",
      },
      {
        value: "其他",
        label: "其他",
      },
    ],
  },
  {
    value: "拼车出行",
    label: "拼车出行",
    children: [
      {
        value: "嘉定校区",
        label: "嘉定校区",
      },
      {
        value: "四平路校区",
        label: "四平路校区",
      },
      {
        value: "沪西校区",
        label: "沪西校区",
      },
      {
        value: "沪北校区",
        label: "沪北校区",
      },
      {
        value: "彰武校区",
        label: "彰武校区",
      },
      {
        value: "铁岭校区",
        label: "铁岭校区",
      },
    ],
  },
  {
    value: "同薅羊毛",
    label: "同薅羊毛",
    children: [
      {
        value: "互助点赞",
        label: "互助点赞",
      },
      {
        value: "拼单团购",
        label: "拼单团购",
      },
      {
        value: "其他",
        label: "其他",
      },
    ],
  },
  {
    value: "其他",
    label: "其他",
  },
];

// const num = ref(1);
const handleChange = (value: number) => {
  console.log(value);
};


const goBack = () => {
  router.push("/home");
  console.log("go back");
};
</script>



<style scoped>
.centered-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  box-sizing: border-box;
}

.large-radius {
  background-color: white;
  width: 100%;
  max-width: 900px;
  border: 1px solid var(--el-border-color);
  border-radius: 10px;
  padding: 25px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.header {
  width: 100%;
  max-width: 900px;
  padding: 20px 30px;
  height: 50px;
  margin-bottom: 20px;
  background-color: #071540d0;
  color: white;
  border-radius: 10px;
  display: flex;
  justify-content: center;
}

.text {
  color: white;
  font-size: 24px;
  display: flex;
  align-items: center;
}

.page-container {
  width: 100%;
}

.form-columns {
  display: flex;
  gap: 30px;
  margin-bottom: 20px;
}

.left-column {
  flex: 1;
  min-width: 0;
}

.right-column {
  width: 250px;
}

.form-item {
  margin-bottom: 20px;
}

.form-item-with-icon {
  display: flex;
  align-items: center;
  gap: 10px;
}

.form-item-with-icon .el-icon {
  font-size: 18px;
  color: #606266;
  flex-shrink: 0;
  vertical-align: text-top; /* 确保图标垂直居中对齐 */
}

.form-item-with-icon .el-input {
  flex: 1;
  height: 36px; /* 保证输入框的高度一致 */
  line-height: 36px; /* 保证输入框的内容垂直居中 */
}

.poster-item {
  margin-bottom: 10px; /* 确保标签与上传区域之间有适当的间距 */
}


.upload-icon {
  font-size: 24px;
  color: #909399;
  margin-bottom: 8px;
}

.upload-text {
  color: #606266;
  font-size: 14px;
  margin-bottom: 4px;
}

.upload-hint {
  color: #909399;
  font-size: 12px;
}





.upload-area:hover {
  border-color: #409eff;
}


.time-picker-group {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
}

.time-separator {
  color: #909399;
  padding: 0 5px;
}

.full-width {
  grid-column: 1 / -1;
}

.form-buttons {
  display: flex;
  justify-content: center; /* 水平居中按钮容器 */
  align-items: center; /* 垂直居中按钮 */
  margin-top: 30px; /* 给按钮添加一些上边距 */
  width: 100%; /* 确保容器占满宽度 */
}

.button-container {
  display: flex;
  margin-left: 350px;
  gap: 20px; /* 按钮之间添加间距 */
  justify-content: center; /* 水平居中按钮 */
}




.el-form-item :deep(.el-form-item__label) {
  font-weight: bold;
}

.form-row {
  display: flex;
  gap: 30px;
  margin-bottom: 20px;
}

.form-column {
  flex: 1;
}

/* 调整海报上传区域样式 */
.poster-upload-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-left: 20px; /* 向右移动上传区域 */
}

.upload-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  min-width: 240px;
  height: 180px;
  border: 1px dashed #dcdfe6;
  border-radius: 6px;
  cursor: pointer;
  transition: border-color 0.3s;
}

.poster-preview {
  width: 240px;         /* 固定宽度，确保预览区域大小一致 */
  height: 180px;        /* 固定高度，确保预览区域大小一致 */
  border: 1px dashed #dcdfe6;
  border-radius: 6px;
  overflow: hidden;
  display: flex;        /* 使用 flexbox 布局来居中图片 */
  justify-content: center; /* 水平居中图片 */
  align-items: center;   /* 垂直居中图片 */
}

.poster-preview img {
  max-width: 100%;      /* 图片最大宽度为容器宽度 */
  max-height: 100%;     /* 图片最大高度为容器高度 */
  object-fit: contain;  /* 保持图片比例，自适应容器大小 */
}


.form-item.full-width {
  width: 100%; /* 使 el-form-item 占满一行 */
}

.form-item.full-width .el-input {
  width: 100%; /* 使 el-input 占满 el-form-item 的宽度 */
}

.demo-ruleForm {
  display: flex;
  flex-direction: column;
}

.form-item-with-icon {
  width: 90%; /* 确保包含图标的容器也占满宽度 */
}

</style>