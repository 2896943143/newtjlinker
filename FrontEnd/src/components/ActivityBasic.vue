<template>
  <div :style="positionStyle" class="activity-card">
    <!-- 海报区域 -->
    <div class="poster-wrapper">
      <img :src="posterUrl" :alt="Name" class="activity-poster" />
    </div>

    <div class="activity-info">
      <div class="info-row name-row">
        <div class="Name" :title="Name">{{ Name }}</div>
      </div>

      <div class="info-row kinds-row">
        <div class="Kinds">
          <el-tag v-for="(Kind, index) in Kinds" :key="index" class="Kind">{{ Kind }}</el-tag>
        </div>
      </div>
      <div class="info-row num-row">
        <div class="Num">人数: {{ Num }}</div>
      </div>
      <div class="info-row date-row">
        <div class="DueDate" :title="`截止时间: ${DueDate}`">截止时间: {{ DueDate }}</div>
      </div>
      <button @click="goToDetails" class="DetailsLink">查看详情 》</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from "vue-router";

const router = useRouter();
const props = defineProps({
  Name: { type: String, required: true },
  Kinds: { type: Array, required: true },
  Num: { type: String, required: true },
  DueDate: { type: String, default: 'auto' },
  ActivityID: { type: String, required: true },
  posterUrl: { type: String, default: '' },
  top: { type: String, default: 'auto' },
  right: { type: String, default: 'auto' },
  bottom: { type: String, default: 'auto' },
  left: { type: String, default: 'auto' }
});

const positionStyle = computed(() => ({
  top: props.top,
  right: props.right,
  bottom: props.bottom,
  left: props.left
}));

const goToDetails = () => {
  localStorage.setItem('activityId', props.ActivityID);
  if (localStorage.getItem('isAdmin') === 'no') {
    router.push("/detail-activity");
  } else {
    router.push("/detail-activity-manager");
  }
};
</script>

<style scoped>
.activity-card {
  position: absolute;
  display: flex;
  flex-direction: row;
  align-items: stretch;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 600px;
  height: 160px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.activity-card:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}
.poster-wrapper {
  flex: none;
  width: 240px;
  height: 160px;
  overflow: hidden;
  transition: transform 0.3s ease;
}
.activity-card:hover .poster-wrapper {
  transform: scale(1.05);
}
.activity-poster {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.activity-info {
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 12px;
  flex: 1;
  min-width: 0;
  row-gap: 15px;            /* 增加行间距 */
  transition: transform 0.3s ease;
}
.activity-card:hover .activity-info {
  transform: scale(1.01);
}
.info-row {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 0;        /* 取消原 margin，改为 row-gap 控制 */
}
.Name {
  position: relative;
  font-size: 18px;
  font-weight: bold;
  padding: 2px 6px;
  color: white;
  z-index: 1;
  transition: font-size 0.3s ease;
}
.Name::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #409EFF;
  border-radius: 4px;
  z-index: -1;
}
.activity-card:hover .Name {
  font-size: 19px;
}
.Kinds {
  display: flex;
  gap: 8px;
  flex-wrap: nowrap;
  transition: transform 0.3s ease;
}
.activity-card:hover .Kinds {
  transform: scale(1.02);
}
.Num, .DueDate {
  font-size: 16px;
  transition: font-size 0.3s ease;
}
.activity-card:hover .Num,
.activity-card:hover .DueDate {
  font-size: 16.5px;
}
.DetailsLink {
  position: absolute;
  right: 12px;
  bottom: 12px;
  color: #409EFF;
  text-decoration: none;
  transition: color 0.3s ease;
}
.activity-card:hover .DetailsLink {
  color: #2a6ebd;
}
</style>
