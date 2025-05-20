<template>
  <div class="event-container">
    <!-- 顶部 Header -->
    <div class="header">
      
      <img src="/Logos/Logo.png" alt="TJLinker Logo" class="logo-image" />
      <div class="user-info">
        <img :src="user.avatarUrl" class="avatar" alt="User Avatar" />
        <div class="user-id">ID: {{ user.id }}</div>
      </div>
    </div>

    <!-- 活动卡片区域 -->
    <div class="event-card">
      <div class="card-title">活动详情</div>

      <div class="event-info-grid">
        <div class="info-row"><span>活动名称：</span><span>{{ event.title }}</span></div>
        <div class="info-row"><span>活动校区：</span><span>{{ event.campus }}</span></div>
        <div class="info-row"><span>活动地点：</span><span>{{ event.location }}</span></div>
        <div class="info-row">
          <span>活动类型：</span>
          <span>
            <el-tag
              v-for="tag in event.tags"
              :key="tag"
              size="small"
              type="success"
            >
              {{ tag }}
            </el-tag>
          </span>
        </div>
        <div class="info-row"><span>活动时间：</span><span>{{ event.time }}</span></div>
        <div class="info-row"><span>报名截止：</span><span>{{ event.registrationDeadline }}</span></div>
        <div class="info-row">
          <span>人数上限：</span>
          <span>{{ event.currentParticipants }}/{{ event.maxParticipants }}</span>
        </div>
        <div class="info-row info-detail-row">
          <span>活动详情：</span>
          <span class="event-desc">{{ event.description }}</span>
        </div>
      </div>

      <!-- 操作区域 -->
      <div class="action-area">
        <el-button type="primary" size="small" @click="enterChatroom">进入聊天室</el-button>
        <el-button type="success" size="small" @click="joinEvent">加入队伍</el-button>
        <el-button type="danger" size="small" @click="quitEvent">退出队伍</el-button>
      </div>
    </div>

    <!-- 底部 poster 插图展示 -->
    <div class="poster-container" v-if="event.posterUrl">
      <img :src="event.posterUrl" alt="活动海报" class="poster-image" />
    </div>

    <!-- 创建者信息 -->
    <div class="footer" @click="PrivateChat">
      创建者：
      <span class="clickable">{{ creator.username }} (ID: {{ event.creatorId }})</span>
    </div>
    
      <el-button class="back-button" type="text" @click="goBack">
        ← 返回
      </el-button>
  </div>
</template>

<script>
import TopNavBarWithoutSearch from "@/components/TopNavBarWithoutSearch.vue";
import router from "@/router";
import { ElTag, ElScrollbar } from "element-plus";

export default {
  components: {
    TopNavBarWithoutSearch,
    ElTag,
    ElScrollbar,
  },
  data() {
    return {
      creator: {
        username: '0',
        avatarUrl: '1', // 获取头像的URL
        id: '2',
      },
      user: {
        username: "111",
        avatarUrl: "",
        id: localStorage.getItem('userId'),
        isAdmin: localStorage.getItem('isAdmin'),
      },
      event: {
        title: "嘉定周末网球双打",
        campus: "嘉定校区",
        location: "嘉定校园网球场",
        category: {
          primary: "体育",
          secondary: "网球",
        },
        time: "2024年10月27日 17:00",
        registrationDeadline: "2024年10月25日 23:59",
        isRealName: true,
        maxParticipants: 4,
        currentParticipants: 3,
        tags: ["# 体育", "# 网球"],
        joinedMembers: [1, 2], // 用户ID数组
        description: "这是活动的详细内容",
        creatorId: "11111111",
      },
      joinStatus: 'notjoined',
      currentDate: new Date(), // 当前日期
    };
  },
  created() {
    this.fetchUserData();
    this.fetchEventDetails();
    this.fetchJoinStatus();
  },
  computed: {
    isRegistrationClosed() {
      // 比较当前时间是否超过报名截止时间
      return new Date(this.event.registrationDeadline) < this.currentDate;
    },
    isParticipantsFull() {
      // 检查当前参与人数是否已满
      return this.event.currentParticipants >= this.event.maxParticipants;
    },
    isCreator() {
      return this.user.id === this.event.creatorId;
    },
  },
  methods: {
    goBack() {
    this.$router.push('/home');
  },
    updateCurrentDate() {
      this.currentDate = new Date();
    },

    enterChatroom() {
      localStorage.setItem('activityName', this.event.title);
      // localStorage.setItem('creatorId', this.event.creatorId);
      // activityId: localStorage.getItem('activityId')
      // userId: localStorage.getItem('userId')
      router.push('/new-chat')
    },

    PrivateChat() {
      if (this.user.id === this.event.creatorId) {
        console.log("当前用户是活动创建者，无法与自己聊天。");
        return;
      }
      localStorage.setItem('another_person', this.event.creatorId);
      // activityId: localStorage.getItem('activityId')
      // userId: localStorage.getItem('userId')
      router.push('/new-chat')
    },

    async fetchJoinStatus() {
      const userId = this.user.id;
      const eventId = localStorage.getItem('activityId'); // activityId
      const url = `http://127.0.0.1:8000/api/get_activity_state/?u_id=${userId}&a_id=${eventId}`;
      try {
        const response = await fetch(url, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        const responseData = await response.json();
        if (responseData.message === 'Activity has been added') {
          this.joinStatus = 'joined';
        }
        else if (responseData.message === 'Activity on hold') {
          this.joinStatus = 'waiting';
        }
        else if (responseData.message === 'Activity not acceded to') {
          this.joinStatus = 'notjoined';
        }
        else if (responseData.message === 'Activity was created by this user') {
          this.joinStatus = 'creator';
        }
      } catch (error) {
        console.error("Fetch operation failed:", error);
        alert("获取活动状态失败！");
      }
      this.updateCurrentDate(); // 刷新当前时间
    },

    async fetchUserData() {
      const userId = localStorage.getItem('userId'); // 替换为你要查询的用户ID
      const url = `http://127.0.0.1:8000/api/users/info?id=${userId}`; // 将userId放在URL查询字符串中
      try {
        const response = await fetch(url, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            // 如果需要，可以在这里添加认证信息，例如：
            //             'Authorization': 'Bearer your-token'
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        this.user = {
          username: data.Name,
          avatarUrl: data.Avatar, // 获取头像的URL
          id: userId,
          isAdmin: localStorage.getItem('isAdmin')
        };
      } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
      }
    },

    async fetchCreatorData() {
      const createorId = this.event.creatorId; // 替换为你要查询的用户ID
      const url = `http://127.0.0.1:8000/api/users/info?id=${createorId}`; // 将userId放在URL查询字符串中
      try {
        const response = await fetch(url, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            // 如果需要，可以在这里添加认证信息，例如：
            //             'Authorization': 'Bearer your-token'
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        this.creator = {
          username: data.Name,
          avatarUrl: data.Avatar, // 获取头像的URL
          id: createorId
        };
      } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
      }
    },

    async fetchEventDetails() {
      const eventId = localStorage.getItem('activityId'); // activityId
      const url = `http://127.0.0.1:8000/api/get_activity_detail/${eventId}`;
      try {
        const response = await fetch(url, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        const responseData = await response.json();
        if (responseData.success) {
          const data = responseData.data;
          // 映射到本地组件的 data 中
          this.event = {
            title: data.Name, // 活动名称
            campus: data.CampusID, // 校区
            location: data.Location, // 地点
            category: {
              primary: data.Class.First, // 一级分类
              secondary: data.Class.Second, // 二级分类
            },
            time: data.StartDate, // 活动开始时间
            registrationDeadline: data.DueDate, // 报名截止时间
            isRealName: data.NeedRealName, // 是否实名
            maxParticipants: parseInt(data.NumLimit), // 人数上限
            currentParticipants: parseInt(data.NumCurrent), // 当前参与人数
            tags: [data.Class.First, data.Class.Second], // 自动生成标签
            joinedMembers: data.Participants.filter((memberId) => memberId), // 参与者ID数组
            description: data.Description, // 活动描述
            creatorId: data.CreatorID, // 创建者ID
            posterUrl: data.PosterUrl || "", // 获取海报URL
          };

          // 调用 fetchCreatorData 获取创建者数据
          await this.fetchCreatorData();
        } else {
          console.error("Failed to fetch event details:", responseData.message);
        }
      } catch (error) {
        console.error("Fetch operation failed:", error);
      }
    },

    async joinActivity() {
      const userId = this.user.id;
      const eventId = localStorage.getItem('activityId'); // activityId
      const url = `http://127.0.0.1:8000/api/join_activity/`;
      const confirmation = confirm("确定要加入活动吗？");
      if (!confirmation) return;
      try {
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            u_id: userId,
            a_id: eventId,
          }), // 将用户ID传递到后端
        });

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        const responseData = await response.json();
        await this.fetchJoinStatus();
        if (responseData.message === 'accept') {
          alert("请求已发送，等待活动创建者确认！");
        } else {
          alert(responseData.message || "加入活动失败！");
        }
      } catch (error) {
        console.error("Fetch operation failed:", error);
        alert("加入活动失败！");
      }
    },

    async handleDissolveTeam() {
      try {
        const confirmation = confirm("确定要解散队伍吗？");
        if (!confirmation) return;

        const eventId = localStorage.getItem('activityId'); // activityId
        const url = `http://127.0.0.1:8000/api/break_activity/`;
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            a_id: eventId,
          }),
        });

        const responseData = await response.json();
        if (responseData.message === 'accept') {
          alert("队伍已解散！");
          // 跳转回活动列表页面或刷新当前页面
          this.$router.push("/home");
        } else {
          alert("解散失败：" + responseData.message);
        }
      } catch (error) {
        console.error("Error dissolving team:", error);
        alert("解散失败，请稍后重试。");
      }
    },

    async Quit() {
      try {
        const confirmation = confirm("确定要退出活动吗？");
        if (!confirmation) return;

        const eventId = localStorage.getItem('activityId'); // activityId
        const userId = localStorage.getItem('userId'); // activityId
        const url = `http://127.0.0.1:8000/api/leave_activity/`;
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            a_id: eventId,
            u_id: userId,
          }),
        });

        const responseData = await response.json();
        if (responseData.message === 'accept') {
          alert("已退出！");
          // 跳转回活动列表页面或刷新当前页面
          this.$router.push("/home");
        } else {
          alert("退出失败：" + responseData.message);
        }
      } catch (error) {
        console.error("Error dissolving team:", error);
        alert("退出失败，请稍后重试。");
      }
    },

  },

  mounted() {
    // 定期更新当前时间，避免用户长时间停留页面后状态不一致
    setInterval(this.updateCurrentDate, 6000);
  },
};
</script>


<style scoped>
.event-container {
  font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
  padding: 32px 20px;
  background: #f9fbfd;
  max-width: 960px;
  margin: auto;
  color: #2c3e50;
}

/* 顶部 header */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 28px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e0e6ed;
}

.logo-image {
  height: 48px;
  object-fit: contain;
}

/* 用户信息样式 */
.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: 2px solid #409EFF;
  object-fit: cover;
}

.user-id {
  font-size: 13px;
  color: #666;
}

/* 活动卡片 */
.event-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
  padding: 28px;
  margin-bottom: 30px;
}

.card-title {
  font-size: 20px;
  font-weight: 600;
  color: #fff;
  background-color: #337ecc;
  padding: 14px 20px;
  border-radius: 10px;
  margin-bottom: 20px;
  text-align: center;
}

/* 信息展示栅格 */
.event-info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  row-gap: 16px;
  column-gap: 32px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  font-size: 15px;
  color: #333;
}

.info-detail-row {
  grid-column: span 2;
  flex-direction: column;
}

.event-desc {
  white-space: pre-wrap;
  margin-top: 8px;
  color: #444;
  line-height: 1.5;
}

/* 操作按钮区域 */
.action-area {
  margin-top: 24px;
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  justify-content: center;
}

/* 海报展示 */
.poster-container {
  margin-top: 32px;
  text-align: center;
}

.poster-image {
  width: 100%;
  max-width: 250px; /* 固定最大宽度 */
  height: auto;
  aspect-ratio: 4 / 3; /* 或者使用固定比例 */
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
  object-fit: contain; /* 确保完整展示不裁剪 */
  margin: 0 auto;
  display: block;
}

/* 页脚创建者信息 */
.footer {
  margin-top: 28px;
  font-size: 14px;
  color: #888;
  text-align: center;
}

.clickable {
  cursor: pointer;
  color: #409EFF;
  font-weight: 500;
}

.clickable:hover {
  text-decoration: underline;
}
.back-button {
  font-size: 14px;
  color: #fff;                      /* 文字颜色改为白色 */
  background-color: #409EFF;        /* 添加背景色 */
  padding: 8px 15px;                /* 增加内边距 */
  border-radius: 4px;               /* 添加圆角 */
  text-decoration: none;            /* 去除下划线 */
  transition: all 0.3s;             /* 添加过渡效果 */
  border: none;                     /* 去除边框 */
  cursor: pointer;                  /* 鼠标悬停指针样式 */
  position: absolute;               /* 绝对定位 */
  right: 420px;                      /* 距离右侧20px */
  top: 800px;                        /* 距离顶部20px */
}

/* 鼠标悬停效果 */
.back-button:hover {
  background-color: #66b1ff;        /* 悬停时背景色变亮 */
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.3); /* 添加阴影效果 */
}
</style>