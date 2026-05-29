using UnityEngine;

//reusable health component that can be attached to any entity (player, enemies, destructible objects) to manage health, damage, and death logic in a consistent way across the game.
public class HealthComponent : MonoBehaviour
{
    [SerializeField] private int _maxHealth = 3;
    private int _currentHealth;

    public int CurrentHealth => _currentHealth;
    public int MaxHealth => _maxHealth;
    public bool IsDead => _currentHealth <= 0;

    private void Awake()
    {
        _currentHealth = _maxHealth;
    }

    public void TakeDamage(int amount)
    {
        if (IsDead) return;

        _currentHealth = Mathf.Max(0, _currentHealth - amount);
        Debug.Log($"{gameObject.name} took {amount} damage. HP: {_currentHealth}/{_maxHealth}");

        if (IsDead)
            OnDeath();
    }

    public void Heal(int amount)
    {
        if (IsDead) return;
        _currentHealth = Mathf.Min(_maxHealth, _currentHealth + amount);
    }

    private void OnDeath()
    {
        Debug.Log($"{gameObject.name} died.");

        // If this is the player, notify everyone
        if (gameObject.CompareTag("Player"))
            EventBus<PlayerDiedEvent>.Publish(new PlayerDiedEvent());
    }
}