using System;
using UnityEngine;

// Reusable health component that can be attached to any entity (player, enemies, destructible objects).
// It only tracks numbers and announces death through the Died event; it does not decide WHAT happens on death.
// The owner (e.g. Entity) subscribes to Died and reacts (destroy itself, trigger game over, play VFX, ...).
public class HealthComponent : MonoBehaviour
{
    [SerializeField] private int _maxHealth = 3;
    private int _currentHealth;

    public int CurrentHealth => _currentHealth;
    public int MaxHealth => _maxHealth;
    public bool IsDead => _currentHealth <= 0;

    // Raised exactly once, on the hit that brings health to 0.
    public event Action Died;

    private void Awake()
    {
        ResetHealth();
    }

    // Public so it can be reused for respawning, and called by EditMode tests (Awake does not run in Edit Mode).
    public void ResetHealth()
    {
        _currentHealth = _maxHealth;
    }

    public void TakeDamage(int amount)
    {
        if (IsDead || amount <= 0) return;

        _currentHealth = Mathf.Max(0, _currentHealth - amount);
        Debug.Log($"{gameObject.name} took {amount} damage. HP: {_currentHealth}/{_maxHealth}");

        if (IsDead)
            Died?.Invoke();
    }

    public void Heal(int amount)
    {
        if (IsDead || amount <= 0) return;
        _currentHealth = Mathf.Min(_maxHealth, _currentHealth + amount);
    }
}
