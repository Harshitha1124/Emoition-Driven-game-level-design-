# Required libraries
from IPython.display import display, Javascript
from google.colab.output import eval_js
from base64 import b64decode
import numpy as np
import cv2
from PIL import Image
import random
from fer import FER

# Function to capture an image from the webcam in Google Colab and close the webcam properly
def take_photo(filename='photo.jpg', quality=0.8):
    js = Javascript('''
    async function takePhoto(quality) {
        const div = document.createElement('div');
        const video = document.createElement('video');
        const button = document.createElement('button');
        button.textContent = 'Capture Photo';
        div.appendChild(video);
        div.appendChild(button);
        document.body.appendChild(div);

        // Request webcam access
        const stream = await navigator.mediaDevices.getUserMedia({video: true});
        video.srcObject = stream;
        await video.play();

        // Resize canvas to match video dimensions
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const context = canvas.getContext('2d');

        // Capture frame and stop webcam
        button.onclick = () => {
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            stream.getTracks().forEach(track => track.stop());  // Stop webcam stream
            div.remove();  // Remove the video element from the DOM
            const data = canvas.toDataURL('image/jpeg', quality);
            return data;
        };

        // Return data URL of the captured image
        const data = await new Promise(resolve => button.onclick = () => {
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            stream.getTracks().forEach(track => track.stop());  // Ensure stream is stopped
            div.remove();  // Remove the video element from the DOM
            resolve(canvas.toDataURL('image/jpeg', quality));
        });
        return data;
    }
    ''')

    display(js)
    data = eval_js('takePhoto({})'.format(quality))
    binary = b64decode(data.split(',')[1])
    with open(filename, 'wb') as f:
        f.write(binary)
    return filename

# Function to detect emotion from an image and visualize the detected face
def detect_emotion(image_path):
    try:
        img = cv2.imread(image_path)
        detector = FER()
        emotions = detector.detect_emotions(img)

        if len(emotions) > 0:
            detected_emotion = emotions[0]['emotions']
            print("Detected emotions scores: ", detected_emotion)  # Debugging information

            # Determine the highest score emotion
            emotion = max(detected_emotion, key=detected_emotion.get)
            score = detected_emotion[emotion]
            print(f"Detected emotion: {emotion} with score: {score:.2f}")

            # If a face is detected, draw a rectangle around it
            for emotion_data in emotions:
                (x, y, w, h) = emotion_data['box']
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.imwrite('emotion_detected.jpg', img)
            img_with_face = Image.open('emotion_detected.jpg')
            img_with_face.show()
            return emotion
        else:
            print("No face detected in the image.")
            return None
    except Exception as e:
        print(f"Emotion detection failed: {e}")
        return None

# Game based on emotion detection
def play_game_based_on_emotion(emotion):
    if not emotion:
        print("Could not detect emotion.")
        return

    print(f"Detected emotion: {emotion}")

    if emotion == "happy":
        print("You're feeling happy! Let's play Rock-Paper-Scissors!")
        rock_paper_scissors()
    elif emotion == "sad":
        print("You're feeling sad. Let's play Snakes and Ladders to cheer you up!")
        snakes_and_ladders()
    elif emotion == "angry":
        print("You're feeling angry. Let's play Tic-Tac-Toe to cool down!")
        tic_tac_toe()
    elif emotion == "fear":
        print("You're feeling fearful. Let's play Riddles!")
        riddles()  # Trigger riddles for fear
    elif emotion == "surprise":
        print("You're feeling surprised! Let's play Guess the Number!")
        guess_the_number()
    elif emotion == "neutral":
        print("You're feeling neutral. Let's play Scrambled Words!")
        scrambled_words_multiple()  # Trigger multiple scrambled words for neutral

# Rock-Paper-Scissors Game
def rock_paper_scissors():
    print("Welcome to Rock-Paper-Scissors!")
    choices = ["rock", "paper", "scissors"]

    while True:
        user_choice = input("Enter rock, paper, or scissors (or 'quit' to exit): ").lower()
        if user_choice == "quit":
            print("Thanks for playing Rock-Paper-Scissors!")
            break

        if user_choice not in choices:
            print("Invalid input. Please choose rock, paper, or scissors.")
            continue

        computer_choice = random.choice(choices)
        print(f"Computer chose: {computer_choice}")

        if user_choice == computer_choice:
            print("It's a tie!")
        elif (user_choice == "rock" and computer_choice == "scissors") or \
             (user_choice == "scissors" and computer_choice == "paper") or \
             (user_choice == "paper" and computer_choice == "rock"):
            print("You win!")
        else:
            print("Computer wins!")

# Snakes and Ladders Game
def snakes_and_ladders():
    print("Welcome to Snakes and Ladders!")

    # Board layout
    board = [i for i in range(1, 101)]
    snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
    ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}
    position = 0  # Player's position

    while True:
        roll = input("Press Enter to roll the dice (or type 'quit' to exit): ")
        if roll.lower() == 'quit':
            print("Thanks for playing Snakes and Ladders!")
            break

        dice_roll = random.randint(1, 6)
        print(f"You rolled a {dice_roll}.")

        position += dice_roll

        if position > 100:
            print("You can't move beyond 100. Stay in your current position.")
            position -= dice_roll  # Move back
            print(f"Your position remains {position}.")
            continue

        # Check for snakes or ladders
        if position in snakes:
            print(f"Oh no! You landed on a snake! Go back to {snakes[position]}.")
            position = snakes[position]
        elif position in ladders:
            print(f"Yay! You found a ladder! Climb up to {ladders[position]}.")
            position = ladders[position]

        print(f"Your current position is {position}.")
        if position == 100:
            print("Congratulations! You've reached the end and won the game!")
            break

# Tic-Tac-Toe Game
def tic_tac_toe():
    print("Welcome to Tic-Tac-Toe!")
    board = [' ' for _ in range(9)]
    current_player = 'X'

    def print_board():
        print(f"{board[0]} | {board[1]} | {board[2]}")
        print("--|---|--")
        print(f"{board[3]} | {board[4]} | {board[5]}")
        print("--|---|--")
        print(f"{board[6]} | {board[7]} | {board[8]}")
        print()

    while True:
        print_board()
        move = input(f"Player {current_player}, enter your move (1-9 or 'quit' to exit): ")

        if move.lower() == 'quit':
            print("Thanks for playing Tic-Tac-Toe!")
            break

        try:
            move = int(move) - 1
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 9.")
            continue

        if move < 0 or move > 8 or board[move] != ' ':
            print("Invalid move. Try again.")
            continue

        board[move] = current_player

        if check_winner(board, current_player):
            print_board()
            print(f"Player {current_player} wins!")
            break

        if ' ' not in board:
            print_board()
            print("It's a tie!")
            break

        current_player = 'O' if current_player == 'X' else 'X'

def check_winner(board, player):
    winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8),
                            (0, 4, 8), (2, 4, 6)]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
            return True
    return False

# Guess the Number Game
def guess_the_number():
    print("Welcome to Guess the Number!")
    number_to_guess = random.randint(1, 20)

    while True:
        guess = input("Guess the number between 1 and 20 (or type 'quit' to exit): ")

        if guess.lower() == 'quit':
            print("Thanks for playing Guess the Number!")
            break

        try:
            guess = int(guess)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if guess < 1 or guess > 20:
            print("Please guess a number between 1 and 20.")
        elif guess < number_to_guess:
            print("Too low! Try again.")
        elif guess > number_to_guess:
            print("Too high! Try again.")
        else:
            print(f"Congratulations! You guessed the number {number_to_guess}.")
            break

# Scrambled Words Game (Multiple for Neutral Emotion)
def scrambled_words_multiple():
    print("Welcome to Scrambled Words! Let's solve multiple scrambled words.")
    words = [
        "apple", "banana", "cherry", "dragon", "elephant", "giraffe", "kiwi", "mango",
        "orange", "peach", "pineapple", "strawberry", "watermelon", "zebra", "avocado",
        "blueberry", "blackberry", "raspberry", "coconut", "grapefruit", "papaya",
        "pomegranate", "persimmon", "nectarine", "tangerine", "jackfruit", "cantaloupe",
        "honeydew", "lime", "lemon", "fig", "date", "prune"
    ]
    random.shuffle(words)

    for word in words:
        scrambled = ''.join(random.sample(word, len(word)))
        print(f"Scrambled word: {scrambled}")
        user_guess = input("Unscramble the word (or type 'quit' to exit): ").lower()

        if user_guess == 'quit':
            print("Thanks for playing Scrambled Words!")
            break

        if user_guess == word:
            print("Correct!")
        else:
            print(f"Wrong! The correct word was {word}.")
        print()

# Riddles Game for Fear Emotion
def riddles():
    print("Welcome to Riddles! Solve the following riddles.")
    riddle_list = [
        ("What has keys but can't open locks?", "keyboard"),
        ("What has a heart but no other organs?", "deck of cards"),
        ("What gets wetter as it dries?", "towel")
    ]

    for riddle, answer in riddle_list:
        print(f"Riddle: {riddle}")
        user_answer = input("Your answer (or type 'quit' to exit): ").lower()

        if user_answer == 'quit':
            print("Thanks for playing Riddles!")
            break

        if user_answer == answer:
            print("Correct!")
        else:
            print(f"Wrong! The correct answer was {answer}.")
        print()

# Main program flow
filename = take_photo()
detected_emotion = detect_emotion(filename)
play_game_based_on_emotion(detected_emotion)