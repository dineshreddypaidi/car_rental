document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('.rental-tab');
    const lists = document.querySelectorAll('.rental-list');

    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // Remove active class from all tabs and lists
            tabs.forEach(t => t.classList.remove('active'));
            lists.forEach(list => list.classList.remove('active'));

            // Add active class to the clicked tab and corresponding list
            this.classList.add('active');
            document.getElementById(this.dataset.target).classList.add('active');
        });
    });
});
