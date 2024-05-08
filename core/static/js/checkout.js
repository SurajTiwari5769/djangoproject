$(document).ready(function () {
    // Add click event listener to address cards
    $(".address-card").click(function () {
        // Remove 'selected' class from all address cards
        $(".address-card").removeClass("selected");
        // Add 'selected' class to the clicked address card
        $(this).addClass("selected");
    });
});