# Transactional-Quantum-Mechanics-Visualizer
For people interested in Transactional interpretations of QM.

Code Breakdown
1. QuantumSystem Class
This class handles the core logic of the simulation. It's responsible for managing the emitters, absorbers, transactions, and the simulation process itself.

__init__ Method:

Initializes the system with a list of emitters and absorbers. It also accepts a boolean use_probabilistic_selection to control whether to use a weighted random selection for transactions.

generate_offer_waves & generate_confirmation_waves:

Offer Waves: These are emitted by the emitters. Each emitter sends out waves (offers) that can later be confirmed by absorbers.

Confirmation Waves: Absorbers confirm the offer waves they interact with. These confirmation waves are stored in the respective transaction.

select_transaction Method:

Transaction Selection: This method selects a transaction (offer wave) that hasn’t been selected yet. If probabilistic selection is enabled, it picks the transaction randomly, weighted by its associated "weight". Otherwise, it picks the transaction with the maximum weight.

Probabilistic Selection: If enabled, it uses random.choices() to select a transaction with a weighted probability. The weights list holds the weight of each unselected transaction. The transaction with the highest weight is selected unless the probabilistic mode is enabled.

update_state & update_positions Methods:

Update State: Sets the system’s state to reflect the result of a selected transaction.

Update Positions: This method updates the positions of the emitters and absorbers based on their velocities.

calculate_total_energy: This method calculates the total energy of the system based on the kinetic energy of the emitters and absorbers.

visualize: Handles the graphical rendering of the system using Pygame. It draws the emitters, absorbers, transaction confirmation waves, particles, and the transaction log on the screen.

2. Emitter and Absorber Classes
Emitter Class: Represents a particle or entity that emits an "offer wave". Each emitter has a position and a velocity. The emit_offer_wave() method creates an offer wave that it can send out.

Absorber Class: Represents an entity that interacts with offer waves. Absorbers confirm offer waves sent by emitters and add them to the transaction.

3. OfferWave and ConfirmationWave Classes
OfferWave: This object represents the wave emitted by the emitter. Each wave can have associated confirmation waves. The weight of the wave depends on the confirmation waves it has accumulated.

ConfirmationWave: This object represents a confirmation from an absorber that interacts with an offer wave.

4. Transaction Log and Visualization
The transaction log in the GUI shows a list of selected transactions. Each entry in the log contains the transaction's weight. The weight is calculated based on the interactions between the offer wave and its confirmation waves.

Transaction Log Explanation
The transaction log provides a record of selected transactions. For each transaction selected, the log stores:

The emitter’s position at the time of selection.

The weight of the transaction.

Example Log Entry:
plaintext
Copy
Edit
Transaction Log:
1: w=40.0
2: w=30.5
3: w=20.3
...
w=40.0 represents the weight of the selected transaction.

The weight value reflects the total weight of confirmation waves (essentially the interaction strength between the emitter and absorbers). In a simple case, the weight might just be based on the number of absorbers confirming a particular wave, or it could involve more complex calculations based on how long or intense the interaction was.

The weight allows us to judge the "strength" or significance of a transaction. If we had more complex interactions, the weight could account for things like:

The number of interactions.

The time or distance traveled by the wave.

Possible Additions/Improvements
Enhance Particle System:

It would be great is people could make the particles more interactive, like having them interact with the waves or even change behavior based on the simulation state. For instance, particles could move towards strong transaction waves.

Track Transaction History:

It might be useful to store more detailed information about each transaction, such as the time at which it was selected, which absorbers interacted with it, and its duration. This could help analyze the simulation over time and provide insights into the behavior of the system.

Improve Transaction Selection Logic:

The probabilistic transaction selection is a good starting point, but could deffo add more complexity, like introducing quantum interference where certain transactions have a greater likelihood of selection based on a combination of their weight and the state of the system.

Add Multiple Transaction Types:

Right now, the system only tracks one type of transaction (wave selection). It could be interesting to introduce different types of transactions that require different interactions or have unique consequences in the simulation.

Advanced Visualization:

The visualization can be further refined. For example, adding a color gradient to the waves based on their weight would make it easier to visualize strong versus weak transactions. 

User-Defined Simulation Parameters:

Allow the user to define the interaction rules between waves and particles. For example, they could set up rules about how absorbers confirm waves (maybe they need to be within a certain distance or meet certain energy thresholds).


TI also suggests that quantum systems are in a superposition of states until a transaction is completed. It might be useful to further refine the model to include the idea of superposition more explicitly, where the emitters and absorbers are in a superposition of possible states (offer waves), and only when they "agree" does the wave collapse into a confirmed state.

Potential Areas for Refinement:
Superposition and Collapse:

TI suggests that the wave is in a superposition until the transaction is completed. Right now, the model has offer waves and confirmation waves, but it might benefit from introducing the superposition principle more directly. For example, offer waves could exist in multiple possible states until an absorber interacts with them, at which point they collapse into a single transaction.


Wave Interference:

In TI, waves can interfere with each other before reaching agreement (i.e., destructive and constructive interference). Introducing a concept of wave interference could make the simulation even closer to TI, as interactions between multiple waves could affect the outcome of the final transaction.


Time Symmetry:

TI involves time symmetry, meaning the offer and confirmation waves exist in a time-symmetric way (i.e., they don't have a clear "cause" and "effect" direction in the way that traditional interpretations of quantum mechanics do). This code currently has a flow where waves are emitted and then confirmed, which is a good approximation. However, to be more in line with the time symmetry of TI, this needs changes been made to the confirmation wave as a retroactive influence on the offer wave. 

Nonlocality and Spacetime:

One aspect of TI is its connection to nonlocality, which suggests that quantum transactions don’t happen in a traditional, locally determined way. Could be helpful to allow nonlocal effects where an emitter and absorber don’t necessarily interact in close proximity, but instead, spacetime interactions and distance affect the strength of waves or the likelihood of a transaction.

Visualizing and Modeling Quantum Events:
Graphical Representation: Using Pygame to visualize the system, which is great. It might be useful to show not only the waves and particles but also superposition states and wave interference to better represent quantum states. Adding a color gradient or similar visualization to indicate the state of superposition or the progression of a transaction might help users connect the abstract concepts of TI with the graphical simulation.

Summary:
The code is fairly close to representing key principles of Transactional Interpretation (like offer and confirmation waves), but it could be improved by adding more explicit superposition, collapse, and wave interference effects.

The probabilistic transaction selection is a good fit for TI’s inherent uncertainty, and the log and visualization systems help track the interactions and final transactions in a way that aligns well with the TI framework.

Happy editing. 
