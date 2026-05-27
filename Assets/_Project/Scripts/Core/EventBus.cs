using System;
using System.Collections.Generic;

public static class EventBus<T> where T : struct
{
    private static readonly List<Action<T>> _handlers = new List<Action<T>>();

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
        for (int i = _handlers.Count - 1; i >= 0; i--)
            _handlers[i].Invoke(evt);
    }
}