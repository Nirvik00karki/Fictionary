// Get the search input element
const searchInput = document.querySelector('input[type="search"]');
// Get all the novel titles
const novelTitles = document.querySelectorAll('h3');

// Function to filter novels based on the search input
const filterNovels = () => {
  const searchTerm = searchInput.value.toLowerCase();
  novelTitles.forEach(title => {
    const novelTitle = title.textContent.toLowerCase();
    if (novelTitle.includes(searchTerm)) {
      title.parentElement.parentElement.style.display = 'block';
    } else {
      title.parentElement.parentElement.style.display = 'none';
    }
  });
};

// Event listener for the search input
searchInput.addEventListener('input', filterNovels);

// Get all the novel image elements
const novelImages = document.querySelectorAll('img[name="myImage"]');

// Function to handle click on novel images
const handleNovelClick = (event) => {
  // Get the clicked image source and extract the novel name
  const novelImageSrc = event.target.src;
  const novelName = event.target.alt;

  // Encode the novel name to be used as a parameter in the URL
  const encodedNovelName = encodeURIComponent(novelName);

  // Construct the URL for the novel details page
  const novelDetailsURL = `novel-details.html?novel=${encodedNovelName}`;

  // Navigate to the novel details page
  window.location.href = novelDetailsURL;
};

// Add click event listener to each novel image
novelImages.forEach(image => {
  image.addEventListener('click', handleNovelClick);
});
