<template>
  <div class="container">
    <h1>真不错热榜聚合</h1>
    
    <div class="rankings-container">
      <div 
        v-for="source in sources" 
        :key="source.id"
        :class="['ranking-section', `source-${source.id}`]"
      >
        <div class="ranking-header">
          <img :src="source.logo" :alt="`${source.title} Logo`" class="ranking-logo">
          <div class="ranking-title">{{ source.title }}</div>
          <button class="refresh-button" @click="loadRankingData(source.id)">刷新</button>
        </div>
        <div class="ranking-content">
          <div v-if="loading[source.id]" class="loading">加载中...</div>
          <div v-else-if="error[source.id]" class="error">{{ error[source.id] }}</div>
          <div v-else-if="rankings[source.id]?.articles?.length === 0" class="no-data">
            暂无数据
          </div>
          <div v-else>
            <div 
              v-for="article in rankings[source.id]?.articles" 
              :key="article.id"
              class="news-item"
            >
              <div class="news-title">
                <span v-if="article.hot_rank >= 0" class="rank-tag">{{ article.hot_rank }}</span>
                <a :href="article.url" target="_blank">{{ article.title }}</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <footer>
      <p>© 2026 真不错科技. All rights reserved. | 
      <a
      href="https://beian.miit.gov.cn/"
      target="_blank"
      rel="noopener"
      class="beian-link"
    >津ICP备2024023329号-3</a></p>
      <p>数据仅供参考，更新时间：{{ updateTime }}</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import axios from 'axios'

const sources = ref([])
const rankings = reactive({})
const loading = reactive({})
const error = reactive({})
const updateTime = ref('')

const apiClient = axios.create({
  baseURL: '/api',  // 使用相对路径，通过 Vite 代理
  timeout: 10000,
})

const updateTimestamp = () => {
  const now = new Date()
  updateTime.value = now.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  })
}

const loadSources = async () => {
  try {
    // 从 URL 获取查询参数
    const searchParams = new URLSearchParams(window.location.search)
    const params = {}

    // 将 URL 参数转换为对象
    searchParams.forEach((value, key) => {
      params[key] = value
    })

    const { data } = await apiClient.get('/sources/', { params })
    sources.value = data.sources
    
    // 加载所有榜单数据
    sources.value.forEach(source => {
      loadRankingData(source.id)
    })
  } catch (err) {
    console.error('加载数据源失败:', err)
  }
}

const loadRankingData = async (sourceId) => {
  loading[sourceId] = true
  error[sourceId] = null
  
  try {
    const { data } = await apiClient.get(`/ranking/${sourceId}/`)
    rankings[sourceId] = data
    updateTimestamp()
  } catch (err) {
    error[sourceId] = '加载失败: ' + (err.response?.data?.error || err.message)
    console.error(`加载榜单${sourceId}失败:`, err)
  } finally {
    loading[sourceId] = false
  }
}

onMounted(() => {
  updateTimestamp()
  loadSources()
})
</script>

<style scoped>
.beian-link {
  color: inherit;
  text-decoration: none;
}
.beian-link:hover {
  text-decoration: underline;
}
</style>