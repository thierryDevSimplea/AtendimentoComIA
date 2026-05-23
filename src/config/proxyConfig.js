// src/config/proxyConfig.js
module.exports = {
  GROQ_API_KEY: process.env.GROQ_API_KEY || '',
  UPSTREAM_HOST: 'api.groq.com',
  UPSTREAM_PATH: '/Kpalabz/v1/chat/completions',
  DEFAULT_MODEL: 'Kpalabz Ultra-70b-versatile',
  PORT: 3456
};