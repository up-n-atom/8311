/**
 * EEPROM Vendor/Part Number Modifier
 *
 * This function modifies SFP EEPROM data to change the vendor name and part number.
 * It generates i2cset commands that can be executed on the device to write the changes.
 *
 * Modified Fields:
 * - Vendor Name (offset 0x14, 16 bytes): Changed to "YV"
 * - Part Number (offset 0x28, 16 bytes): Changed to "SFP+ONU-XGSPON"
 * - Checksum (offset 0x3F, 1 byte): Recalculated to maintain EEPROM integrity
 *
 * Why "YV" and "SFP+ONU-XGSPON"?
 * These values are used because they represent the earliest supported ONU to make it into
 * the Linux kernel, ensuring broad compatibility and driver support.
 *
 * Checksum Note:
 * We only recalculate and write the first checksum at offset 0x3F (covering bytes 0x00-0x3E)
 * because this function only modifies fields within that range. The second checksum at
 * offset 0x5F (covering bytes 0x40-0x5E) is not modified since we don't write any bytes
 * beyond offset 0x3F.
 *
 * Input: Base64-encoded EEPROM data (must decode to exactly 256 bytes)
 * Output: Series of i2cset commands to unlock EEPROM, write changes, and reboot
 */
function generate_eeprom_vendor() {
    // Get selected device type
    const deviceType = document.querySelector('input[name="device-type"]:checked').value;

    // Constants
    const VENDOR_ID = "YV";
    const VENDOR_PN = "SFP+ONU-XGSPON";

    // Unlock command based on device type
    const unlockCommand = deviceType === "WAS-110"
        ? 'i2cset -fy 0 0x51 0x7B 0x12 0x34 0x56 0x78 i'
        : 'i2cset -fy 0 0x51 0x7B 0x91 0x42 0xF0 0x07 i';

    // Helper function to write padded string to data
    function writeString(data, offset, str, length) {
        const padded = (str + ' '.repeat(length)).substring(0, length);
        return data.substring(0, offset) + padded + data.substring(offset + length);
    }

    // Helper function to generate i2cset command
    function generateCommand(data, offset, length) {
        const hex = [];
        for (let i = 0; i < length; i++) {
            hex.push('0x' + data.charCodeAt(offset + i).toString(16).padStart(2, '0'));
        }
        return `i2cset -fy 0 0x50 0x${offset.toString(16).padStart(2, '0')} ${hex.join(' ')} i`;
    }

    // Main processing logic
    const input = document.getElementById('eeprom-base64').value.replace(/[\s\n\r]/g, '');
    const output = document.getElementById('eeprom-output');

    // Remove the hidden style from output area, we will display errors here too
    output.closest('div').removeAttribute('style');

    try {
        // Decode base64
        let data = atob(input);

        if (data.length !== 256) {
            output.textContent = `Error: Data is ${data.length} bytes, expected 256`;
            return;
        }

        // Modify vendor and part number
        data = writeString(data, 0x14, VENDOR_ID, 16);
        data = writeString(data, 0x28, VENDOR_PN, 16);

        // Calculate and write checksum
        let sum = 0;
        for (let i = 0; i < 0x3F; i++) sum += data.charCodeAt(i);
        const checksum = sum % 256;
        data = data.substring(0, 0x3F) + String.fromCharCode(checksum) + data.substring(0x40);

        // Generate commands
        const commands = [
            '# Unlock EEPROM',
            unlockCommand,
            `# Write Vendor Name "${VENDOR_ID}" (offset 0x14, 16 bytes)`,
            generateCommand(data, 0x14, 16),
            `# Write Part Number "${VENDOR_PN}" (offset 0x28, 16 bytes)`,
            generateCommand(data, 0x28, 16),
            `# Write Checksum 0x${checksum.toString(16).padStart(2, '0')} (offset 0x3F, 1 byte)`,
            generateCommand(data, 0x3F, 1),
            '# Reboot',
            'reboot'
        ];

        output.textContent = commands.join('\n');
    } catch (e) {
        output.textContent = 'Error: ' + e.message;
    }
}
