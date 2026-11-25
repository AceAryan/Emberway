using System;
using System.Collections.Generic;
using UnityEngine;

// Global, type-safe publish/subscribe. Each event struct type T gets its own independent handler list.
// Usage:
//   OnEnable:  EventBus<PlayerDiedEvent>.Subscribe(HandlePlayerDied);
//   OnDisable: EventBus<PlayerDiedEvent>.Unsubscribe(HandlePlayerDied);
//   Anywhere:  EventBus<PlayerDiedEvent>.Publish(new PlayerDiedEvent());
public static class EventBus<T> where T : struct
{
    private static readonly List<Action<T>> _handlers = new List<Action<T>>();

    // Runs once, the first time EventBus<T> is used for this T.
    static EventBus()
    {
        EventBusRegistry.Register(Clear);
    }

    public static void Subscribe(Action<T> handler)
    {
        if (!_handlers.Contains(handler))
            _handlers.Add(handler);
    }

    public static void Unsubscribe(Action<T> handler)
    {
        _handlers.Remove(handler);
    }

    public static void Publish(T evt)
    {
        // Iterate over a snapshot so handlers may Subscribe/Unsubscribe while we're publishing.
        Action<T>[] snapshot = _handlers.ToArray();
        foreach (Action<T> handler in snapshot)
        {
            // One broken handler must not stop the others from receiving the event.
            try { handler.Invoke(evt); }
            catch (Exception e) { Debug.LogException(e); }
        }
    }

    public static void Clear()
    {
        _handlers.Clear();
    }
}

// Non-generic helper: a generic class can't carry [RuntimeInitializeOnLoadMethod] for every T,
// so each EventBus<T> registers its Clear() here, and we clear them all when Play Mode starts.
// This matters when "Enter Play Mode Options" disables domain reload: statics would otherwise
// keep handlers from destroyed objects of the previous play session.
internal static class EventBusRegistry
{
    private static readonly List<Action> _clearActions = new List<Action>();

    internal static void Register(Action clear)
    {
        _clearActions.Add(clear);
    }

    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
    private static void ClearAll()
    {
        foreach (Action clear in _clearActions)
            clear();
    }
}
