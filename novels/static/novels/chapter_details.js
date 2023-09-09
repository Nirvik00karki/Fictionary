// Function to toggle visibility of an element
function toggleVisibility(elementId) {
  var element = document.getElementById(elementId);
  element.classList.toggle('hidden');
}

// Event listeners for icons
document.getElementById('bookmark-icon').addEventListener('click', function() {
  window.location.href = '/library';
});

document.getElementById('settings-icon').addEventListener('click', function() {
  toggleVisibility('settings-dialog');
});

document.getElementById('day-night-icon').addEventListener('click', function() {
  // Code to toggle between day and night mode
});

// Event listener for close button in settings dialog
document.getElementById('close-settings').addEventListener('click', function() {
  toggleVisibility('settings-dialog');
});
