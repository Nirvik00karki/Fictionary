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