using NUnit.Framework;
using UnityEngine;

// EditMode tests: run instantly without entering Play Mode.
// Note: Awake() does NOT run for components added in Edit Mode, so we call ResetHealth() ourselves.
public class HealthComponentTests
{
    private GameObject _go;
    private HealthComponent _health;

    [SetUp]
    public void SetUp()
    {
        _go = new GameObject("TestEntity");
        _health = _go.AddComponent<HealthComponent>();
        _health.ResetHealth(); // default max health = 3
    }

    [TearDown]
    public void TearDown()
    {
        Object.DestroyImmediate(_go);
    }

    [Test]
    public void StartsAtMaxHealth()
    {
        Assert.AreEqual(_health.MaxHealth, _health.CurrentHealth);
        Assert.IsFalse(_health.IsDead);
    }

    [Test]
    public void TakeDamage_ReducesHealth()
    {
        _health.TakeDamage(1);
        Assert.AreEqual(_health.MaxHealth - 1, _health.CurrentHealth);
    }

    [Test]
    public void TakeDamage_ClampsAtZero()
    {
        _health.TakeDamage(999);
        Assert.AreEqual(0, _health.CurrentHealth);
        Assert.IsTrue(_health.IsDead);
    }

    [Test]
    public void TakeDamage_NegativeAmount_IsIgnored()
    {
        _health.TakeDamage(-5);
        Assert.AreEqual(_health.MaxHealth, _health.CurrentHealth);
    }

    [Test]
    public void Died_FiresExactlyOnce()
    {
        int diedCount = 0;
        _health.Died += () => diedCount++;

        _health.TakeDamage(_health.MaxHealth); // lethal
        _health.TakeDamage(1);                 // already dead, must not fire again

        Assert.AreEqual(1, diedCount);
    }

    [Test]
    public void Died_DoesNotFire_OnNonLethalDamage()
    {
        bool died = false;
        _health.Died += () => died = true;

        _health.TakeDamage(_health.MaxHealth - 1);

        Assert.IsFalse(died);
    }

    [Test]
    public void Heal_ClampsAtMax()
    {
        _health.TakeDamage(1);
        _health.Heal(999);
        Assert.AreEqual(_health.MaxHealth, _health.CurrentHealth);
    }

    [Test]
    public void Heal_WhenDead_DoesNothing()
    {
        _health.TakeDamage(999);
        _health.Heal(1);
        Assert.AreEqual(0, _health.CurrentHealth);
    }
}
