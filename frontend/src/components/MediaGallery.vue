<template>
  <div class="media-gallery">
    <div v-if="images.length > 0" class="images-container">
      <div
        v-for="(image, index) in images"
        :key="image.id"
        class="media-item image-item"
        @click="openImageModal(index)"
      >
        <img
          :src="image.file_url"
          :alt="`Image ${index + 1}`"
          loading="lazy"
          class="media-image"
        />
      </div>
    </div>

    <div v-if="videos.length > 0" class="videos-container">
      <div
        v-for="video in videos"
        :key="video.id"
        class="media-item video-item"
      >
        <video
          :src="video.file_url"
          controls
          class="media-video"
          preload="metadata"
        >
          Your browser does not support the video tag.
        </video>
      </div>
    </div>

    <!-- Image Modal -->
    <div v-if="showImageModal" class="image-modal" @click="closeImageModal">
      <button class="modal-close" @click="closeImageModal">×</button>
      <button class="modal-nav modal-prev" @click.stop="prevImage" v-if="images.length > 1">‹</button>
      <button class="modal-nav modal-next" @click.stop="nextImage" v-if="images.length > 1">›</button>
      <img
        :src="images[currentImageIndex].file_url"
        alt="Full size image"
        class="modal-image"
        @click.stop
      />
      <div class="image-counter" v-if="images.length > 1">
        {{ currentImageIndex + 1 }} / {{ images.length }}
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'MediaGallery',
  props: {
    media: {
      type: Array,
      required: true,
    },
  },
  setup(props) {
    const showImageModal = ref(false)
    const currentImageIndex = ref(0)

    const images = computed(() => {
      return props.media.filter(m => m.media_type === 'image')
    })

    const videos = computed(() => {
      return props.media.filter(m => m.media_type === 'video')
    })

    const openImageModal = (index) => {
      currentImageIndex.value = index
      showImageModal.value = true
      document.body.style.overflow = 'hidden'
    }

    const closeImageModal = () => {
      showImageModal.value = false
      document.body.style.overflow = ''
    }

    const nextImage = () => {
      currentImageIndex.value = (currentImageIndex.value + 1) % images.value.length
    }

    const prevImage = () => {
      currentImageIndex.value = (currentImageIndex.value - 1 + images.value.length) % images.value.length
    }

    return {
      images,
      videos,
      showImageModal,
      currentImageIndex,
      openImageModal,
      closeImageModal,
      nextImage,
      prevImage,
    }
  },
}
</script>

<style scoped>
.media-gallery {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.images-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.5rem;
}

.image-item {
  cursor: pointer;
  overflow: hidden;
  border-radius: 4px;
  aspect-ratio: 1;
}

.media-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.2s;
}

.image-item:hover .media-image {
  transform: scale(1.05);
}

.videos-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.video-item {
  width: 100%;
}

.media-video {
  width: 100%;
  max-height: 500px;
  border-radius: 4px;
  background-color: #000;
}

/* Image Modal */
.image-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  cursor: pointer;
}

.modal-image {
  max-width: 90%;
  max-height: 90%;
  object-fit: contain;
}

.modal-close {
  position: absolute;
  top: 20px;
  right: 30px;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  font-size: 2rem;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
}

.modal-close:hover {
  background: rgba(255, 255, 255, 0.3);
}

.modal-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  font-size: 3rem;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
}

.modal-nav:hover {
  background: rgba(255, 255, 255, 0.3);
}

.modal-prev {
  left: 30px;
}

.modal-next {
  right: 30px;
}

.image-counter {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  color: white;
  background: rgba(0, 0, 0, 0.5);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .images-container {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  }

  .modal-nav {
    width: 50px;
    height: 50px;
    font-size: 2rem;
  }

  .modal-prev {
    left: 10px;
  }

  .modal-next {
    right: 10px;
  }
}
</style>
