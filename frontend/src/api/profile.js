import api from './index'

export const getProfile    = ()     => api.get('users/profile/')
export const updateProfile = (data) => api.patch('users/profile/', data)