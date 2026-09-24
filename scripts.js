// ========== 分类切换逻辑 ==========
document.addEventListener('DOMContentLoaded', () => {
  const navBtns = document.querySelectorAll('.nav-btn');
  const sections = document.querySelectorAll('.content-section');
  const modal = document.getElementById('imageModal');
  const modalImg = document.getElementById('modalImg');
  const modalClose = document.querySelector('.modal-close');
  const backToTopBtn = document.getElementById('backToTop');

  // 图片加载状态处理
  const galleryImages = document.querySelectorAll('.gallery-item img');
  galleryImages.forEach(img => {
    img.addEventListener('load', () => {
      img.classList.add('loaded');
      img.parentElement.classList.add('img-loaded');
    });

    // 如果图片已经加载完成
    if (img.complete) {
      img.classList.add('loaded');
      img.parentElement.classList.add('img-loaded');
    }
  });

  // 视频懒加载和播放控制
  const videos = document.querySelectorAll('.video-item video');
  videos.forEach(video => {
    const videoItem = video.parentElement;

    // 视频加载完成后移除加载提示
    video.addEventListener('loadeddata', () => {
      videoItem.classList.add('video-loaded');
    });

    // 点击播放时才加载视频
    video.addEventListener('click', () => {
      if (video.readyState === 0) {
        video.load();
      }
    });

    // 鼠标悬停时预加载视频
    videoItem.addEventListener('mouseenter', () => {
      if (video.readyState === 0) {
        video.load();
      }
    });

    // 视频播放时暂停其他视频
    video.addEventListener('play', () => {
      videos.forEach(v => {
        if (v !== video) v.pause();
      });
    });
  });

  // 回到顶部按钮
  window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
      backToTopBtn.classList.add('show');
    } else {
      backToTopBtn.classList.remove('show');
    }
  });

  backToTopBtn.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });

  // 分类切换
  navBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const category = btn.dataset.category;
      navBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      sections.forEach(section => section.classList.remove('active'));
      document.getElementById(category).classList.add('active');
    });
  });

  // 图片预览
  const galleryItems = document.querySelectorAll('.gallery-item');
  galleryItems.forEach(item => {
    item.addEventListener('click', () => {
      const img = item.querySelector('img');
      if (img) {
        modalImg.src = img.src;
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
      }
    });
  });

  // 关闭模态框
  modalClose.addEventListener('click', closeModal);
  modal.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
  });

  // ESC 关闭
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('show')) closeModal();
  });

  function closeModal() {
    modal.classList.remove('show');
    document.body.style.overflow = '';
  }

  // 触摸滑动切换分类
  let touchStartX = 0;
  const activeSection = document.querySelector('.content-section.active');
  const categories = ['dishes', 'environment', 'videos'];

  activeSection.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
  }, { passive: true });

  activeSection.addEventListener('touchend', (e) => {
    const touchEndX = e.changedTouches[0].screenX;
    const threshold = 50;
    const currentIndex = categories.indexOf(activeSection.id);

    if (touchStartX - touchEndX > threshold && currentIndex < categories.length - 1) {
      switchCategory(categories[currentIndex + 1]);
    } else if (touchEndX - touchStartX > threshold && currentIndex > 0) {
      switchCategory(categories[currentIndex - 1]);
    }
  }, { passive: true });

  function switchCategory(category) {
    navBtns.forEach(btn => {
      btn.classList.remove('active');
      if (btn.dataset.category === category) btn.classList.add('active');
    });
    sections.forEach(section => section.classList.remove('active'));
    document.getElementById(category).classList.add('active');
  }

  console.log('🍽️ 广东美食网站已加载');
});
