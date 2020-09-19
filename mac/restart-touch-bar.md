# Restart Apple TouchBar

## Description

Very often, I find myself with a TouchBar that does not work as expected. Some icons don't appear, it is not responsive to the open applications, etc. But, most frustrating I hate it when the media button disappears. This is sometimes resolved by restarting Apple Music app. The below command will force the TouchBar to restart and hopefully fix any glitches.

## Resolution

* Restart TouchBar (requires sudo access).

```bash
sudo pkill TouchBarServer && sudo killall “ControlStrip”
```