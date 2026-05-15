import api from './index'

export const getAllPosts = () => api.get('/posts/')
export const getPost = (id) => api.get(`/posts/${id}/`)
export const createPost = (formData) => api.post('/posts/', formData)
export const updatePost = (id, data) => api.patch(`/posts/${id}/`, data)
export const deletePost = (id) => api.delete(`/posts/${id}/`)
export const getAllTags   = () => api.get('/tags/')