<template>
    <a :href="url" class="image-button" :style="{ width, height, borderRadius: borderRadius || '30px'}" @click="handleClick">
      <img :src="imageSrc" :alt="altText" class="image-button__image" />
    </a>
  </template>
  
  <script setup lang="ts">
  import { defineProps } from 'vue';
  
  interface ButtonProps {
    url: string;
    imageSrc: string;
    altText: string;
    width?: string;
    height?: string;
    borderRadius?: string;
    onClick?: () => void;
  }
  
  const props = defineProps<ButtonProps>();
  
  const handleClick = (event: Event) => {
    if (props.onClick) {
      event.preventDefault();
      props.onClick();
    }
  };
  </script>
  
  <style scoped>
  .image-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    cursor: pointer;
    transition: box-shadow 0.25s;
  }
  
  .image-button:hover {
    box-shadow: 2px 4px 8px rgba(0, 0, 0, 0.2);
  }
  
  .image-button__image {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  </style>