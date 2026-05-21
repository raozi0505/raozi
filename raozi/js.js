// 1. 轮播图核心逻辑
const carouselInner = document.querySelector('.carousel-inner');
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');
let currentIndex = 0;
const itemCount = document.querySelectorAll('.carousel-item').length;

// 切换轮播图函数
function changeCarousel(index) {
    currentIndex = index;
    carouselInner.style.transform = `translateX(-${currentIndex * (100 / itemCount)}%)`;
}

// 上一张/下一张按钮事件
prevBtn.addEventListener('click', () => {
    currentIndex = (currentIndex - 1 + itemCount) % itemCount;
    changeCarousel(currentIndex);
});

nextBtn.addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % itemCount;
    changeCarousel(currentIndex);
});

// 自动轮播（3秒切换一次）
setInterval(() => {
    currentIndex = (currentIndex + 1) % itemCount;
    changeCarousel(currentIndex);
}, 3000);