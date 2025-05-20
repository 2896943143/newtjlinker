<template>
  <div class="page-container">
    <!-- 新增海报容器 -->
    <div class="activity-card-list">
      <!-- 海报属性说明 -->
      <ActivityBasic
        v-for="(activity, index) in activities"
        :key="activity.ActivityID"
        :Name="activity.Name"
        :Kinds="activity.Kinds"
        :Num="activity.Num"
        :DueDate="activity.DueDate"
        :ActivityID="activity.ActivityID"
        :posterUrl="activity.posterUrl"
        :top="index % 2 === 0 ? `${index * 60 - 15}px` : `${(index-1) * 60 - 15}px`"
        :left="index % 2 === 0 ? '30px' : '680px'"
        :right="index % 2 === 0 ? '700px' : '30px'"
      />
    </div>

    <!-- 分页组件 -->
    <el-pagination
      layout="prev, pager, next"
      :total="total"
      :page-size="pageSize"
      :current-page="currentPage"
      @current-change="handlePageChange"
      class="pagination"
    />
  </div>
</template>

<script setup lang='ts'>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import ActivityBasic from "@/components/ActivityBasic.vue"

const props = defineProps({
  firstCategory: {
    type: String,
    required: true
  },
  secondCategory: {
    type: String,
    required: true
  },
  searchKeyword: {
    type: String,
    required: false,
    default: ''
  },
  user_id: {
    type: String,
    required: true
  },
  currentMenu: {
    type: String,
    required: true
  }
});

const activities = ref<any[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = 10

// 修改API请求参数
const fetchActivities = async (page: number, keyword: string, category: string, user_id: string, currentMenu: string) => {
  try {
    const url = currentMenu === '1' 
      ? "http://127.0.0.1:8000/api/search_and_filter_activities/"
      : "http://127.0.0.1:8000/api/search_and_filter_dingyueactivities/";

    const params = {
      word: keyword,
      page: page.toString(),
      pageSize: pageSize.toString(),
      category: category,
      user_id: user_id,
      includePoster: true // 新增参数标记
    };

    const queryParams = new URLSearchParams(params).toString();
    const encodedUrl = `${url}?${queryParams}`;

    const response = await axios.get(encodedUrl);
    
    if (response.data.success) {
      // 处理响应数据，添加海报URL
      activities.value = response.data.data.map(activity => ({
        ...activity,
        posterUrl: activity.PosterUrl || '' // 根据实际API字段调整
      }));
      total.value = response.data.total;
    } else {
      activities.value = [];
      total.value = 0;
    }
  } catch (error) {
    console.error('Error fetching activities:', error);
    activities.value = [];
    total.value = 0;
  }
}

const handlePageChange = (page: number) => {
  currentPage.value = page;
  fetchActivities(page, props.searchKeyword, getCategory(), props.user_id, props.currentMenu);
}

const getCategory = () => {
  return [props.firstCategory, props.secondCategory]
    .filter(Boolean)
    .join(',') || '全部';
}

onMounted(() => {
  fetchActivities(currentPage.value, props.searchKeyword, getCategory(), props.user_id, props.currentMenu);
})

watch([() => props.firstCategory, () => props.secondCategory, () => props.searchKeyword], ([newFC, newSC, newKW]) => {
  fetchActivities(currentPage.value, newKW, getCategory(), props.user_id, props.currentMenu);
});
</script>

<style scoped>
/* 新增海报容器样式 */
.activity-card-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 60px; /* 为分页留出空间 */
}

/* 保持原有样式 */
.pagination {
  height: 10px;
  padding: 16px; 
  margin-top: 20px; /* 调整分页位置 */
  justify-content: center;
}
</style>