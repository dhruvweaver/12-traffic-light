#include <SFML/Graphics.hpp>
#include <iostream>

// Function to open the image
void openImage(const std::string& filename, sf::RenderWindow &window) {
    sf::Texture texture;
    if (!texture.loadFromFile(filename)) {
        std::cerr << "Error loading image" << std::endl;
        return;
    }
    sf::Sprite sprite(texture);
    window.draw(sprite);
    window.display();
}

// Function to close the image window
void closeImage(sf::RenderWindow &window) {
    window.close();
}

int main() {
    sf::RenderWindow window(sf::VideoMode(800, 600), "Image Viewer");
    // Open the image
    openImage("light_0.jpg", window);

    // Wait for the user to press enter
    std::cout << "Press Enter to close the window..." << std::endl;
    std::cin.ignore();

    // Close the image
    closeImage(window);

    return 0;
}

